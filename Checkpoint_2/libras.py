import cv2
import mediapipe as mp
import time
import os

# Menu de boas-vindas
print("============================")
print("  RECONHECIMENTO DE VOGAIS ")
print("        EM LIBRAS")
print("============================")
print("[1] Usar WEBCAM")
print("[2] Usar VÍDEO MP4")
opcao = input("Escolha uma opção: ")

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

if opcao == '1':
    cap = cv2.VideoCapture(0)
elif opcao == '2':
    video_path = os.path.join(os.getcwd(),'Checkpoint_2', 'assets', 'video', 'mao_direita.mp4')
    print("Caminho do vídeo:", video_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        exit()
else:
    print("Opção inválida. Encerrando o programa.")
    exit()

# Função para identificar as vogais em Libras baseado na posição dos dedos
def detectar_vogal(landmarks):
    def is_polegar_open(finger_tip, finger_mcp):
        return finger_tip.x < finger_mcp.x  # Para mão direita (mude para < se usar mão esquerda)

    def is_finger_up(finger_tip, finger_mcp):
        return finger_tip.y < finger_mcp.y

    polegar_up = is_polegar_open(landmarks[4], landmarks[2])
    indicador_up = is_finger_up(landmarks[8], landmarks[5])
    medio_up = is_finger_up(landmarks[12], landmarks[9])
    anelar_up = is_finger_up(landmarks[16], landmarks[13])
    mindinho_up = is_finger_up(landmarks[20], landmarks[17])

    if not indicador_up and not medio_up and not anelar_up and not mindinho_up and polegar_up:
        return 'A'
    elif indicador_up and medio_up and anelar_up and mindinho_up and polegar_up:
        return 'O'
    elif indicador_up and medio_up and anelar_up and mindinho_up and not polegar_up:
        return 'E'
    elif not indicador_up and not medio_up and not anelar_up and mindinho_up and not polegar_up:
        return 'I'
    elif indicador_up and medio_up and not anelar_up and not mindinho_up and not polegar_up:
        return 'U'
    else:
        return "Não identificado"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo ou erro ao carregar.")
        break

    frame = cv2.resize(frame, (500, 500))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            vogal = detectar_vogal(hand_landmarks.landmark)

            if vogal:
                cv2.putText(frame, f'Vogal detectada: {vogal}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print(f'Vogal detectada: {vogal}')

    cv2.imshow("Video", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()