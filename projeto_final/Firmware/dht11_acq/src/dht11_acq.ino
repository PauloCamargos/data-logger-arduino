/**
* Federal University of Uberlândia
* DataBase Project
* repo: github.com/paulocamargos/data-logger-arduino
*
* Connections:
*  Conecte pino 1 do sensor (esquerda) ao +5V
*  Conecte pino 2 do sensor ao pino de dados definido em seu Arduino
*  Conecte pino 4 do sensor ao GND
*  Conecte o resistor de 10K entre pin 2 (dados)
*  e ao pino 1 (VCC) do sensor
*/

#include "DHT.h" // library download at: https://github.com/adafruit/DHT-sensor-library
// also download the dependency: https://github.com/adafruit/Adafruit_Sensor
// put the file Adafruit_Sensor.h inside the folder lib/DHT-sendor-library
//////////
//Pinos //
//////////
#define PINO_VENTILADOR 13
#define PINO_IRRIGADOR  12
#define DHTPIN A1 // pino que estamos conectado
#define DHTTYPE DHT11 // DHT 11

/////////////
//Comandos //
/////////////
#define CMD_LIGAR_VENTILADOR    'T'
#define CMD_DESLIGAR_VENTILADOR 't'

#define CMD_LIGAR_IRRIGADOR     'U'
#define CMD_DESLIGAR_IRRIGADOR  'u'

#define CMD_LER_DADOS           'R'

////////////////
//Comunicação //
////////////////
#define COMM_UMIDADE        'U'
#define COMM_TEMPERATURA    'T'
#define COMM_END_1          '\r'
#define COMM_END_2          '\n'

////////////////
//Global Data //
////////////////
char cmd_serial;
float read_temp, fake_umid;
DHT dht(DHTPIN, DHTTYPE);

void setup(){
    Serial.begin(9600);
    pinMode(PINO_VENTILADOR, OUTPUT);
    pinMode(PINO_IRRIGADOR, OUTPUT);
    dht.begin();
}

void loop(){
    if(Serial.available()){
        cmd_serial = Serial.read();
        switch(cmd_serial){
            case CMD_LIGAR_VENTILADOR:
            digitalWrite(PINO_VENTILADOR, HIGH);
            break;
            case CMD_DESLIGAR_VENTILADOR:
            digitalWrite(PINO_VENTILADOR, LOW);
            break;
            case CMD_LIGAR_IRRIGADOR:
            digitalWrite(PINO_IRRIGADOR, HIGH);
            break;
            case CMD_DESLIGAR_IRRIGADOR:
            digitalWrite(PINO_IRRIGADOR, LOW);
            break;
            case CMD_LER_DADOS:
            // A leitura da temperatura e umidade pode levar 250ms!
            // O atraso do sensor pode chegar a 2 segundos.
            read_temp = dht.readTemperature();
            fake_umid = dht.readHumidity();
            // if (isnan(t) || isnan(h)) {
            //   Serial.println("Failed to read from DHT");
            // }
            Serial.write(COMM_TEMPERATURA);
            Serial.print(read_temp, 2);
            Serial.write(COMM_END_1);
            Serial.write(COMM_END_2);
            Serial.write(COMM_UMIDADE);
            Serial.print(fake_umid, 2);
            Serial.write(COMM_END_1);
            Serial.write(COMM_END_2);
            break;
        }
    }
}
