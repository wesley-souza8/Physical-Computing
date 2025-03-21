## 1. Instalação das Bibliotecas Necessárias

### **Se estiver usando os computadores da FIAP:**

1. Abra o **Anaconda Navigator**.
![ANACONDA NAVIGATOR](/aula20250307/assets/img/AnacondaNavigator.png)
2. No **CMD.exe Prompt**, execute os seguintes comandos:

### **Se estiver no seu próprio computador:**

No terminal, execute:

```sh
pip install opencv-python
pip install matplotlib
pip install notebook
pip install pyserial  # Integração do Arduino com Python
pip install mediapipe
pip install --upgrade mediapipe opencv-python numpy
pip install matplotlib opencv-python notebook pyserial mediapipe
```

## 2. Componentes Usados no Circuito

Os seguintes componentes são utilizados no projeto:

- **Arduino Uno**
- **Board**
- **Led Amarelo**
- **Led Verde**
- **Led Vermelho**
- **3 Resistores**

O circuito montado no SimulIDE ficará assim:

![Circuito no SimulIDE](/aula20250321/assets/img/circuito.png)

### **Configuração da Porta Serial no Código**
No arquivo **face.py**, edite a linha **8** para corresponder porta informada pelo arduino IDE (exemplo: **COM5**):

```python
arduino = serial.Serial('COM5', 9600, timeout=1)
```

## 3. Usando Webcam ou MP4

O código principal é **face.py**.

Existem duas formas de rodar o código, dependendo da entrada de vídeo desejada.

### **1. Usar a Webcam**
Se deseja utilizar a webcam para detecção, altere a linha **18** do código **face.py**, substituindo `video_path` por `0`:

```python
cap = cv2.VideoCapture(0)
```

### **2. Usar um Vídeo MP4**
Caso prefira utilizar um vídeo pré-gravado, mantenha a variável `video_path`

```python
cap = cv2.VideoCapture(video_path)
```

## 4. Executando o Código
Aula de hoje foi para mostrar uma funcionalidade do MediaPipe, com o reconhecimento dos olhos.
O mediaPipe identifica os valores do olho aberto e do olho fechado.
Quando o olho está aberto, o led verde fica ligado.
Quando o olho está piscando, o led amarelo fica ligado e caso o olho fique muito tempo fechado, o led vermelho acenderá.

```python
if ear <= LIMIAR_FECHAR:
    frames_fechado += 1

    if frames_fechado == 3:
        piscadas += 1
        arduino.write(b'Y')  # Piscada = LED verde (normal)

    elif frames_fechado > LIMIAR_COCHILO:
        arduino.write(b'R')  # Cochilo detectado = LED vermelho + buzzer

elif ear > LIMIAR_ABRIR:
    frames_fechado = 0
    arduino.write(b'G')  # Olhos abertos = estado normal
```

1. Execute o código arduino.py no terminal:
    ```sh
    python face.py
    ```

## 5. Observações Finais

* Caso o vídeo não abra, verifique se o arquivo selfie.mp4 está localizado corretamente em assets/vid/.



