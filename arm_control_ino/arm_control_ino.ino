#include <Servo.h>
#include <math.h>

Servo servo0;
Servo servo1;
Servo servo2;
//Servo servo3;
Servo servo4;
  
void initial(){
  
  //Initial Configuration  
  servo0.write(90);
  servo1.write(90);
  servo2.write(140);
  //servo3.write(40);
  servo4.write(115);
  delay(2000);
}

void lift(){
  
  int i, j, k;
  Serial.println("Lifting");
  for(i = 90 ; i <= 135 ; i+=5){
    servo1.write(i);
    delay(50);
  }
  
    for(i = 140 ; i >= 75 ; i-=5){
    servo2.write(i);
    delay(30);
  }
    for(i = 135, j = 75 ; i <= 170 || j<=140 ; i+=5, j+=10){
      if(i<=170)    
        servo1.write(i);
      delay(20);
      if(j<=140)
        servo2.write(j);
    delay(20);
  }
  
  delay(1000);
  servo4.write(50);
  delay(2000);
  
  for(i = 170, j = 140 ; i >= 45 || j >= 15 ; i-=4, j-=4){
    
    servo2.write(j);
    delay(30);
    servo1.write(i);
    delay(30);
  }
}
  
void setup(){
  
  servo0.attach(3);
  servo1.attach(5);
  servo2.attach(6);
  //servo3.attach(9);
  servo4.attach(10);
  
  Serial.begin(9600);
  Serial.println("Ready");
  
  initial();
 // lift();
}
  
void loop(){

  char Byte = ' ';
  char str[2];
  if(Serial.available()){
      char Byte = Serial.read();
      str[0] = Byte;
      str[1] = '\0';
      Serial.println(str);
      if(strcmp(str,"G") == 0) {
          Serial.println("Almost");
          lift();    
          exit(0);
        }
  }
}  
  
 
 
