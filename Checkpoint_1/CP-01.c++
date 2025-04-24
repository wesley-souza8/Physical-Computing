#include <DHT.h>
#include <ArduinoJson.h>
#include <Servo.h>

#define dhtpin 2
#define servoPin 6
#define dhttype DHT11

Servo myServo;

DHT dht(dhtpin, dhttype);

void setup() {
    Serial.begin(9600);
    dht.begin();
    myServo.attach(servoPin);
}

void loop() {
    int temperatura = dht.readTemperature();
    temperatura = (temperatura * 1.8) + 32;
    int umidade = dht.readHumidity();

    StaticJsonDocument<100>json;
    json["temperatura"] = temperatura;
    json["umidade"] = umidade;
    serializeJson(json, Serial);

    Serial.println();
    delay(3000);

    if (Serial.available() > 0) {
        char comando = Serial.read();

        if (comando == '1'){
            myServo.write(0);
            
        }else if (comando == '2'){
            myServo.write(90);
            
        }else if (comando == '3'){
            myServo.write(180);
        }
    }
}