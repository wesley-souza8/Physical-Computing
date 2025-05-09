import numpy as np

#Tabela verdade AND
entradas = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
saidas = np.array([0, 1, 1, 1])

#pesos e bias
pesos = np.zeros(2)
bias = 0.0
taxa_aprendizado = 0.1
epocas = 10

def ativacao(soma):
    return 1 if soma >= 1 else 0

#Treinamento do perceptron
for _ in range(epocas):
    for i in range(len(entradas)):
        x = entradas[i]
        y = saidas[i]
        soma = np.dot(x, pesos) + bias
        saida = ativacao(soma)
        erro = y - saida
        pesos += taxa_aprendizado * erro * x
        bias += taxa_aprendizado * erro

# Exporta para um arquivo .h (Arduino)
with open("modelo_perceptron_and.h", "w") as f:
    f.write("// Pesos e bias do modelo AND treinado em Python\n")
    f.write("float pesos[2] = {%.6f, %.6f};\n" % (pesos[0], pesos[1]))
    f.write("float bias = %.6f;\n" % bias)

print("Pesos treinados:", pesos)
print("Bias treinado:", bias)
