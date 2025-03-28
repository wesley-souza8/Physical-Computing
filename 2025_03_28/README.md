## 1. Instalação das Bibliotecas Necessárias

### **Se estiver usando os computadores da FIAP:**

1. Abra o **Anaconda Navigator**.
![ANACONDA NAVIGATOR](/2025_03_28/assets/img/anacondaNavigator.png)
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
pip install matplotlib notebook opencv-python pyserial mediapipe numpy
```

## 2. Componentes Usados no Circuito

Os seguintes componentes são utilizados no projeto:

- **Arduino Uno**
- **Board**
- **Led Verde**
- **1 Resistor**

O circuito montado ficará assim:

![Circuito](/2025_03_28/assets/img/circuito.png)

## 3. Usando Webcam ou MP4

O código principal é **video_pose.py**.

Existem duas formas de rodar o código, dependendo da entrada de vídeo desejada.

### **1. Usar a Webcam**
Se deseja utilizar a webcam para detecção, altere a linha **11** do código **video_pose.py**, substituindo `video_path` por `0`:

```python
cap = cv2.VideoCapture(0)
```

### **2. Usar um Vídeo MP4**
Caso prefira utilizar um vídeo pré-gravado, mantenha a variável `video_path`

```python
cap = cv2.VideoCapture(video_path)
```

## 4. Executando o Código

### Objetivo da Demonstração
Implementar um sistema de reconhecimento de movimentos utilizando MediaPipe para monitorar exercícios de rosca direta, com feedback visual via Arduino.

### Funcionamento do Sistema

1. **Reconhecimento Corporal**:
   - MediaPipe identifica pontos-chave do membro superior esquerdo:
     - Ombro
     - Cotovelo
     - Punho

2. **Contagem de Repetições**:
   - Analisa o movimento angular entre as articulações
   - Contabiliza cada repetição completa do exercício

3. **Feedback Visual**:
   - Sistema inicia com todos os LEDs apagados
   - Ao atingir 12 repetições completas:
     - ✅ LED verde é acionado como sinal de conclusão

### Fluxo de Operação
```mermaid
graph TD
    A[MediaPipe detecta articulações] --> B{Ângulo do cotovelo}
    B -->|Movimento válido| C[Incrementa contador]
    C --> D{Contador = 12?}
    D -->|Sim| E[Aciona LED verde]
    D -->|Não| F[Continua monitoramento]

```python
if contador == 12:
    arduino.write(b'G')  
```

4. **Execute o código arduino.py no terminal**:
    ```sh
    python video_pose.py
    ```

## 5. Observações Finais

* Caso o vídeo não abra, verifique se o arquivo selfie.mp4 está localizado corretamente em assets/vid/.



