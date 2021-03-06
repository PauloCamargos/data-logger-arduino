//////////
//Pinos //
//////////
#define PINO_VENTILADOR 13
#define PINO_IRRIGADOR  12

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
float fake_temp, fake_umid;

void setup(){
    Serial.begin(9600);
    pinMode(PINO_VENTILADOR, OUTPUT);
    pinMode(COMM_TEMPERATURA, OUTPUT);
    fake_temp = 15;
    fake_umid = 10;
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
            Serial.write(COMM_TEMPERATURA);
            Serial.print(fake_temp, 2);
            Serial.write(COMM_END_1);
            Serial.write(COMM_END_2);
            Serial.write(COMM_UMIDADE);
            Serial.print(fake_umid, 2);
            Serial.write(COMM_END_1);
            Serial.write(COMM_END_2);
            fake_temp += 2.5;
            fake_umid += 7.5;
            if(fake_umid > 90){
                fake_umid = 10;
            }
            if(fake_temp > 50){
                fake_temp = 15;
            }
            break;
        }
    }
}
