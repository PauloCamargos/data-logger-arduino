#define TEMPERATURE A0
#define UMIDITY     A1

float read_temperature;
float read_umidity;
char read_serial;

void setup() {
    Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
    read_temperature = (analogRead(TEPERATURE) * 5.0 / 1023.0) * 0.1; //Given in oC, 0.1 converts V -> oC 
    read_umidity = (analogRead(UMIDITY) / 1023.0 * 100); //Given in percentage.
    read_serial = Serial.read();
    if(read_serial == 'T'){
      Serial.println("T: " + String(read_temperature, 2));        
    }else if(read_serial == 'U'){
      Serial.println("U: " + String(read_umidity, 2));
    }
  }
}

