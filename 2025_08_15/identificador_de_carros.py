
import cv2
import numpy as np

# ========= CONFIGS RÁPIDAS  =========
VIDEO_PATH = "./2025_08_15/Carros.mp4"   # ou 0 para webcam
SAVE_OUTPUT = False
OUTPUT_PATH = "saida_annotada.mp4"

# Canny (faixas)
CANNY_LOW = 80
CANNY_HIGH = 200
GAUSS_KERNEL = (1, 1)

# Hough (linhas de faixa)
HOUGH_RHO = 1
HOUGH_THETA = np.pi / 180
HOUGH_THRESH = 50
HOUGH_MIN_LINE_LEN = 40
HOUGH_MAX_LINE_GAP = 120

# ROI em percentuais (trapézio): top mais estreito, bottom mais largo
ROI_TOP_Y = 0.55     # altura da parte de cima do trapézio
ROI_BOTTOM_Y = 0.95  # altura da parte de baixo
ROI_TOP_XL = 0.35    # canto superior esquerdo (mais para o centro)
ROI_TOP_XR = 0.65    # canto superior direito (mais para o centro)


# MOG2 (carros em movimento)
MOG_HISTORY = 500
MOG_VARTHRESH = 25
MIN_CONTOUR_AREA = 800   # filtra ruído (ajustar conforme cena)
KERNEL_CLOSE = (5, 5)

# ===============================================================

def region_mask(shape, top_y, bottom_y, top_xl, top_xr):
    h, w = shape[:2]
    pts = np.array([[
        (int(w*0.05), int(h*bottom_y)),             # canto inferior esquerdo
        (int(w*top_xl), int(h*top_y)),               # topo esquerdo
        (int(w*top_xr), int(h*top_y)),               # topo direito
        (int(w*0.95), int(h*bottom_y))               # canto inferior direito
    ]], dtype=np.int32)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, pts, 255)
    return mask, pts

def draw_lane_lines(frame, edges):
    # ROI
    mask, pts = region_mask(
        frame.shape, ROI_TOP_Y, ROI_BOTTOM_Y, ROI_TOP_XL, ROI_TOP_XR
    )
    edges_roi = cv2.bitwise_and(edges, mask)

    # Hough
    lines = cv2.HoughLinesP(
        edges_roi, HOUGH_RHO, HOUGH_THETA, HOUGH_THRESH,
        minLineLength=HOUGH_MIN_LINE_LEN, maxLineGap=HOUGH_MAX_LINE_GAP
    )

    overlay = frame.copy()
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            cv2.line(overlay, (x1, y1), (x2, y2), (0, 255, 0), 4)

    # desenha ROI
    cv2.polylines(overlay, pts, isClosed=True, color=(255, 255, 0), thickness=2)

    # mistura com transparência
    out = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    return out

def detect_moving_cars(frame, fg_mask):
    # limpa ruído
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, KERNEL_CLOSE)
    clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel, iterations=2)
    clean = cv2.dilate(clean, kernel, iterations=1)

    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < MIN_CONTOUR_AREA:
            continue
        x, y, w, h = cv2.boundingRect(c)
        aspect = w / float(h + 1e-5)
        # filtro simples de proporção/área (ajustável)
        if 0.8 <= aspect <= 4.0:
            boxes.append((x, y, w, h))
    return boxes, clean

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Não consegui abrir o vídeo/câmera:", VIDEO_PATH)
        return

    # writer opcional
    writer = None

    # background subtractor (funciona melhor com câmera fixa)
    mog2 = cv2.createBackgroundSubtractorMOG2(history=MOG_HISTORY, varThreshold=MOG_VARTHRESH, detectShadows=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # redimensionar opcional (descomente se seu vídeo for 4K, por ex.)
        frame = cv2.resize(frame, (300, 300))

        # --- FAIXAS: Blur + Canny + Hough ---
        blur = cv2.GaussianBlur(frame, GAUSS_KERNEL, 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, CANNY_LOW, CANNY_HIGH)

        lanes = draw_lane_lines(frame, edges)

        # --- CARROS EM MOVIMENTO: MOG2 + contornos ---
        fg = mog2.apply(blur)          # usar blur ajuda a estabilizar a máscara
        boxes, clean_mask = detect_moving_cars(frame, fg)

        annotated = lanes.copy()
        for (x, y, w, h) in boxes:
            cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(annotated, "carro", (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2, cv2.LINE_AA)

        # janelas auxiliares (pode fechar se quiser algo minimalista)
        cv2.imshow("preview - anotado", annotated)
        cv2.imshow("edges (Canny)", edges)
        cv2.imshow("fgmask (MOG2)", clean_mask)

        # inicializa writer ao ver o primeiro frame
        if SAVE_OUTPUT and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = annotated.shape[:2]
            writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, cap.get(cv2.CAP_PROP_FPS) or 30.0, (w, h))

        if writer is not None:
            writer.write(annotated)

        key = cv2.waitKey(30) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()