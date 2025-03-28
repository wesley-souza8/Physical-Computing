import cv2                          # Biblioteca para vídeo e imagens
import mediapipe as mp              # Biblioteca do Google para reconhecimento corporal
import numpy as np
import serial
import os                  # Para cálculos matemáticos (vetores e ângulos)

# Inicializa o modelo de detecção de pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils  # Para desenhar na tela

arduino = serial.Serial('COM5', 9600, timeout=1)

# Contador de repetições
contador = 0
fase = None  # 'descendo' ou 'subindo'

video_path = os.path.join(os.getcwd(), '2025_03_28', 'assets', 'vid', 'exercicio.mp4')

# Abre a webcam
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()          # Captura o vídeo frame a frame
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Volta ao início do vídeo
        continue
        #break
    frame = cv2.resize(frame, (500, 500))
    frame = cv2.flip(frame, 1)       # Espelha o vídeo (efeito espelho)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB (MediaPipe espera RGB)
    resultado = pose.process(rgb)    # Processa a pose no frame atual

    if resultado.pose_landmarks:     # Se algum corpo for detectado
        mp_draw.draw_landmarks(frame, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Pegando os pontos do braço direito
        pontos = resultado.pose_landmarks.landmark
        ombro = [pontos[12].x * frame.shape[1], pontos[12].y * frame.shape[0]]     # Ponto do ombro direito
        cotovelo = [pontos[14].x * frame.shape[1], pontos[14].y * frame.shape[0]]  # Cotovelo direito
        punho = [pontos[16].x * frame.shape[1], pontos[16].y * frame.shape[0]]     # Pulso direito

        # Cálculo direto do ângulo entre ombro, cotovelo e punho
        a = np.array(ombro)
        b = np.array(cotovelo)
        c = np.array(punho)

        angulo = np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) -
                            np.arctan2(a[1]-b[1], a[0]-b[0]))
        angulo = np.abs(angulo)
        if angulo > 180:
            angulo = 360 - angulo

        # Exibe o ângulo na tela
        cv2.putText(frame, f"Angulo: {int(angulo)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Lógica da repetição
        if angulo > 160:
            fase = 'descendo'
        if angulo < 40 and fase == 'descendo':
            fase = 'subindo'
            contador += 1

        if contador == 12:
            arduino.write(b'G')        

        # Exibe o número de repetições
        cv2.putText(frame, f"Repeticoes: {contador}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostra o vídeo com as informações
    cv2.imshow("Rosca Biceps - Pose Detection", frame)

    # Encerra se apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza a aplicação
cap.release()
cv2.destroyAllWindows()