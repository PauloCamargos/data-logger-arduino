/**
  Federal University of Uberlândia
  DataBase Project
  repo: github.com/paulocamargos/data-logger-arduino

  Connections:
   Conecte pino 1 do sensor (esquerda) ao +5V
   Conecte pino 2 do sensor ao pino de dados definido em seu Arduino
   Conecte pino 4 do sensor ao GND
   Conecte o resistor de 10K entre pin 2 (dados)
   e ao pino 1 (VCC) do sensor
*/

#include "DHT.h" // library download at: https://github.com/adafruit/DHT-sensor-library
// also download the dependency: https://github.com/adafruit/Adafruit_Sensor
// put the file Adafruit_Sensor.h inside the folder lib/DHT-sendor-library
//////////
//Pinos //
//////////
#define PINO_UMIDIFICADOR  12
#define DHTPIN A1 // pino que sensor Ar esta conectado
#define HIGOPIN A2 // pino que o sensor de solo esta conectado
#define DHTTYPE DHT11 // tipo de sensor

/////////////
//Comandos //
/////////////
  
#define CMD_LIGAR_UMIDIFICADOR     'U'
#define CMD_DESLIGAR_UMIDIFICADOR  'u'

#define CMD_LER_TEMPERATURA         'T'
#define CMD_LER_UMIDADE_AR          'A'
#define CMD_LER_UMIDADE_SOLO         'S'

////////////////
//Global Data //
////////////////
char cmd_serial;
float read_temp, read_umid_ar, read_umid_solo;

DHT dht(DHTPIN, DHTTYPE); // dth(pino, tipo)

void setup() {
  Serial.begin(9600);
  pinMode(PINO_UMIDIFICADOR, OUTPUT);
  dht.begin();
}

void loop() {
  if (Serial.available()) {
    cmd_serial = Serial.read();
    switch (cmd_serial) {
      case CMD_LIGAR_UMIDIFICADOR:
        digitalWrite(PINO_UMIDIFICADOR, HIGH);
        break;
      case CMD_DESLIGAR_UMIDIFICADOR:
        digitalWrite(PINO_UMIDIFICADOR, LOW);
        break;
      case CMD_LER_TEMPERATURA:
        read_temp = dht.readTemperature();
//        if(isnan(read_temp/))
          Serial.println(read_temp, 2);
        break;
      case CMD_LER_UMIDADE_AR:
        read_umid_ar = dht.readHumidity();
//         if(isnan(read_umid_ar))/
           Serial.println(read_umid_ar, 2);
         break;
      case CMD_LER_UMIDADE_SOLO:
        read_umid_solo = analogRead(HIGOPIN)/1023.0;
        read_umid_solo = (1 - read_umid_solo) * 100;
        Serial.println(read_umid_solo);
        break;
    }
  }
}
