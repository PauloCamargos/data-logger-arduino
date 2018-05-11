#define TEMPERATURE A0
#define UMIDITY     A1

float read_temperature;
float read_umidity;
char read_serial;

void setup() {
  Serial.begin(9600);
}

void loop() {
  read_temperature = (analogRead(TEMPERATURE) * 5.0 / 1023.0) / 0.01; //Given in oC, 0.1 converts V -> oC
  read_umidity = (analogRead(UMIDITY) / 1023.0 * 100); //Given in percentage.
  if (Serial.available() > 0) {
    read_serial = Serial.read();
    //    Serial.println(read_serial);
    if (read_serial == 'T') {
      Serial.println(read_temperature);
    } else if (read_serial == 'U') {
      Serial.println(read_umidity);
    }
  }
}

