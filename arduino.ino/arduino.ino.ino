#define SYNC 2
#define BEAMSHUTTERPIN 4
#define LIGHTPIN 8

void setup() {
    pinMode(SYNC, INPUT);
    pinMode(BEAMSHUTTERPIN, OUTPUT);
    pinMode(LIGHTPIN, OUTPUT);
    //pinMode(LED_BUILTIN, OUTPUT);
    while(!Serial){;}
    
    Serial.begin(115200);
    //clear everything that might have come after the control char
    while(Serial.available() > 0){
      char t = Serial.read();
    }  
}


void loop() {  
  int shots = 0;
  char serialListener = '0';
  if (Serial.available()) {
    serialListener = Serial.read();
    switch(serialListener){
      case 'O':
        shutterOpen(true);
        break;
      case 'C':
        shutterOpen(false);
        break;
      case 'L':
        digitalWrite(LIGHTPIN, HIGH);
        break;
      case 'F':
        digitalWrite(LIGHTPIN, LOW);
        break;  
      case 'N':
        shots = Serial.parseInt();
        exposeNShots(shots); 
        break;
      case 'D':
        shots = Serial.parseInt();
        delay(100);
        exposeNShots(shots);
        break;
      case 'T':
        Serial.println('1');
        break;
      default:
        break;      
    }
    serialListener = '0';
    
    
    //clear everything that might have come after the control char
    while(Serial.available() > 0){
      char t = Serial.read();
    }       
  }
}


void exposeNShots(int shots){   
  int val = 0;
  int val_last = 1; 
  int count = 0;
  digitalWrite(BEAMSHUTTERPIN, LOW);//close it just in case it is open
  bool opened = false;
  
  while (count <= shots){
    val = digitalRead(SYNC);
    if (val == 1 and val_last == 0){ //falling egdge - our signal to operate
      if (opened == false){
        delay(3); //wait 3 ms for the right moment (shutting takes ~11ms)
        digitalWrite(BEAMSHUTTERPIN, HIGH);
        opened = true;
        count++;
      }
      else if (opened == true){
        count++;
      }
    }//end falling edge
    val_last = val;
    
  }//end while
  delay(2); //closing is a bit slower
  digitalWrite(BEAMSHUTTERPIN, LOW);
}


void shutterOpen(bool state){ 
  //int val = 0;
  //int val_last = 1; 
  //while (true){
  // val = digitalRead(SYNC);
  // if (val == 1 and val_last == 0){
  //  break; // breaks on a rising edge
  // }
  // val_last = val;
 //}
  if (state) {
      digitalWrite(BEAMSHUTTERPIN, HIGH);
  }
  if (! state){
      digitalWrite(BEAMSHUTTERPIN, LOW);
  }
}
