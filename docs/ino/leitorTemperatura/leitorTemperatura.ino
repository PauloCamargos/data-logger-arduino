#define TEMPERATURE A3
#define UMIDITY     A1

float read_temperature;
float read_umidity;
char read_serial;

void setup() {
  Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
         read_serial = Serial.read();
    if (read_serial == 'T') {
         read_temperature = (analogRead(TEMPERATURE) * 5.0 / 1023.0);// / 0.01; //Given in oC, 0.1 converts V -> oC
         Serial.println(read_temperature);
    } else if (read_serial == 'U') {
      read_umidity = (analogRead(UMIDITY)/ 1023.0 )* 100; //Given in percentage.
      Serial.println(read_umidity);
    }
  }
}

