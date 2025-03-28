#define Greenled 8
 
void setup() {
  
  Serial.begin(9600);
  pinMode(Greenled,OUTPUT);
 
}
 
void loop() {

  if(Serial.available() > 0){

    char comando = Serial.read();

    if(comando == 'G'){

        digitalWrite(Greenled, HIGH);

    } else {

        digitalWrite(Greenled, LOW);

    }
  }

}