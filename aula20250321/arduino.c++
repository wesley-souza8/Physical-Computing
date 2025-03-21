#define Greenled 2
#define Yellowled 8
#define Redled 12

 
void setup() {
  
  Serial.begin(9600);
  pinMode(Greenled,OUTPUT);
  pinMode(Yellowled,OUTPUT);
  pinMode(Redled,OUTPUT);
 
}
 
void loop() {

  if(Serial.available() > 0){

    char comando = Serial.read();

    if(comando == 'G'){

        digitalWrite(Greenled, HIGH);
        digitalWrite(Redled, LOW);
        digitalWrite(Yellowled, LOW);

    } else if (comando == 'Y'){

        digitalWrite(Greenled, LOW);
        digitalWrite(Redled, LOW);
        digitalWrite(Yellowled, HIGH);

    } else if (comando == 'R'){

        digitalWrite(Greenled, LOW);
        digitalWrite(Redled, HIGH);
        digitalWrite(Yellowled, LOW);

    }
  }

}