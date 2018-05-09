
#define CMD_LIGAR_VENTILADOR    'T'
#define CMD_DESLIGAR_VENTILAR   't'
#define CMD_LIGAR_IRRIGADOR     'U'
#define CMD_DESLIGAR_IRRIGADOR  'u'

#define PINO_VENTILADOR 13
#define PINO_IRRIGADOR  12

char cmd_serial;
void setup(){
    Serial.begin(9600);
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
        }
    }

}
