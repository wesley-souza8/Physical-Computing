import cv2
import mediapipe as mp
import serial
import time

# Configurar a porta serial (ajuste para a porta correta do seu Arduino)
arduino = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)  # Aguarda a inicialização da conexão serial

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Abrir um vídeo MP4
video_path = "video.mp4"  # Substitua pelo caminho do seu vídeo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo ou erro ao carregar.")
        break

    # Redimensiona o vídeo para 500x500
    frame = cv2.resize(frame, (500, 500))

    # Converte para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detecta a posição do dedo indicador (índice 8)
            index_finger_y = hand_landmarks.landmark[8].y

            # Define comandos baseados na posição do dedo
            if index_finger_y < 0.5:  # Dedo levantado
                arduino.write(b'1')  # Move para 90°
            else:  # Dedo abaixado
                arduino.write(b'2')  # Move para 180°

    cv2.imshow("Video", frame)

    # Aguarda um pouco para sincronizar com a taxa de quadros do vídeo
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()