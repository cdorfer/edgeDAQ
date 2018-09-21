#include <Adafruit_MAX31865.h>

#define LIGHTPIN 9
#define BEAMSHUTTERPIN 12

Adafruit_MAX31865 max = Adafruit_MAX31865(2, 3, 4, 5);
#define RREF      4300.0
#define RNOMINAL  1000.0



void setup() {
    pinMode(LIGHTPIN, OUTPUT);
    pinMode(BEAMSHUTTERPIN, OUTPUT);
    Serial.begin(9600);
    max.begin(MAX31865_2WIRE);
    while (!Serial){
      ;
    }
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        switch(serialListener){
          case 'O':
            shutterOpen(true);
            break;
          case 'C':
            shutterOpen(false);
            break;
          case 'L':
            lightOn(true);
            break;
          case 'D':
            lightOn(false);
            break;
          case 'T':
            returnTemperature();
            break;
          default:
            break;
        }
    }
}

void shutterOpen(bool state){
  if (state) {
    digitalWrite(BEAMSHUTTERPIN, HIGH);
  }
  if (! state){
    digitalWrite(BEAMSHUTTERPIN, LOW);
  } 
}

void lightOn(bool state){
  if (state) {
    digitalWrite(LIGHTPIN, HIGH);
  }
  if (! state){
    digitalWrite(LIGHTPIN, LOW);
  }
}


float returnTemperature(){
  uint16_t rtd = max.readRTD();
  uint8_t fault = max.readFault();
  if (!fault) {
    Serial.println(max.temperature(RNOMINAL, RREF));
  }
  else {
    Serial.println(9000);
    max.clearFault();
  }
}
