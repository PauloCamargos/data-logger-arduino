const int potenciometro = 0; 
int valor = 0;
char opcao;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    opcao = Serial.read();
    if(opcao == '1')
    {
      valor = analogRead(potenciometro);  
      Serial.println(valor);
    }
  } 
}
