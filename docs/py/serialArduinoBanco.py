#!/usr/bin/python
# Importanto a biblioteca para comunicacao com o postgreSQL
import psycopg2
import time
import serial

print "Teste"
class Banco:
    con = None
    cur = None
    query = None

    def connection(self):
        try:
            print('Conectando com o banco de dados ...')
            self.con = psycopg2.connect(database="aula", 
            user="postgres", password="banco",
            host='localhost',port=5432)

            self.cur = self.con.cursor()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)      

    def insertData(self, value):
        self.cur.execute("INSERT INTO aulas.tb_log(valor) VALUES (" + str(value) + ")")   
        self.con.commit()    
    
    def closeConnecetion(self):
        self.con.close()

class Arduino:
    # Iniciando conexao serial
    
    #comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao
    # Parametro enviado para o arduino
    PARAM_CARACTER='1'                
    valorArduino = 0

    def recebeDados(self):
        self.comport = serial.Serial('/dev/ttyACM0', 9600)
        #enviando o comando para o arduino
        self.comport.write(self.PARAM_CARACTER)
        time.sleep(1.8)
        self.valorArduino = self.comport.readline()
        print self.valorArduino
        self.comport.close()     


def main():
    print('Vamo!!!')
    myDB = Banco()
    #myArduino = Arduino()
    #myArduino.recebeDados()

    myDB.connection()
    comport = serial.Serial('/dev/ttyACM0', 9600)
    #comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao
    
    PARAM_CARACTER='1'
    
    for i in range(1,10):
        time.sleep(1.8) # Entre 1.5s a 2s
        comport.write(PARAM_CARACTER)
        VALUE_SERIAL=comport.readline()        
        print '\nRetorno da serial: %s' % (VALUE_SERIAL)        
    #   myArduino.recebeDados()
        myDB.insertData(VALUE_SERIAL)
    #   time.sleep(1)
    
    # Fechando conexao serial
    comport.close()   
    myDB.closeConnecetion()


if __name__ == "__main__":
    main()