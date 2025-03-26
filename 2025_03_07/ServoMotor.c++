#include<Servo.h>

#define servoPin 6

Servo myServo;

void setup() {

  Serial.begin(9600);
  myServo.attach(servoPin);

}

void loop() {
  if (Serial.available() > 0) {

    char comando = Serial.read();

    if (comando == '1'){
        myServo.write(90);

    }else if (comando == '2'){
        myServo.write(180);
        
    }
  }

}
