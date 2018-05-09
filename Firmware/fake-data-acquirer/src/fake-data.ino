

char cmd_serial;
void setup(){
    Serial.begin(9600);
}

void loop(){
    if(Serial.available()){
        cmd_serial = Serial.read();

    }

}
