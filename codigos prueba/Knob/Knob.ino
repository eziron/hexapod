#include <Servo.h>

Servo myservo;  

#define potpin A0
int val;    
unsigned long sum = 0;
unsigned long n_sum = 0;
unsigned long ms = 0;
void setup() {
  Serial.begin(115200);
  myservo.attach(6);  // attaches the servo on pin 9 to the servo object
  ms = millis();
}

void loop() {
  sum += analogRead(potpin); 
  n_sum++;

  if(millis()-ms>50){
    ms = millis();
    
    val = map(sum/n_sum, 0, 1023, 500, 2500);   
    myservo.writeMicroseconds(val); 
    Serial.println(val);

    n_sum = 0;
    sum = 0;
  }     
}
