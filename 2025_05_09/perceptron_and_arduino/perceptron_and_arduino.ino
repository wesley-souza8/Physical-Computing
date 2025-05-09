#include "modelo_perceptron_and.h"

const int pinoLedSaida = 13;

void setup() {
  pinMode(pinoLedSaida, OUTPUT);
  Serial.begin(9600);
  Serial.println("Digite as entradas (0 ou 1) ");
}

int ativacao(float soma) {
  return (soma >= 1) ? 1 : 0;
}

void loop() {
  if (Serial.available() >= 3) {
    char entradaA = Serial.read();   // Primeiro 
    Serial.read();                   // Espaço (ignorado)
    char entradaB = Serial.read();   // Segundo 

    if ((entradaA != '0' && entradaA != '1') || (entradaB != '0' && entradaB != '1')) {
      Serial.println("Erro: digite apenas 0 ou 1");
      while (Serial.available()) Serial.read(); 
      return;
    }

    int a = entradaA - '0';
    int b = entradaB - '0';

    float soma = a * pesos[0] + b * pesos[1] + bias;
    int saida = ativacao(soma);

    digitalWrite(pinoLedSaida, saida ? HIGH : LOW);
    Serial.print("Entrada: ");
    Serial.print(a); Serial.print(" ");
    Serial.print(b); Serial.print(" -> Saida (AND): ");
    Serial.println(saida);

    while (Serial.available()) Serial.read(); 
  }
}
