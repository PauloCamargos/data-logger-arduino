import psycopg2
import time
import serial

print ("Iniciando programa...")

class Banco:
    con = None
    cur = None
    query = None

    def connection(self):
        try:
            print('Conectando com o banco de dados ...')
            self.con = psycopg2.connect(database="projects",
            user="postgres", password="banco",
            host='localhost',port=5432)

            self.cur = self.con.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insertData(self, value):
        # self.cur.execute("INSERT INTO aulas.tb_log(valor) VALUES (" + str(value) + ")")
        self.cur.execute("INSERT INTO arduinoproject.environment(description) VALUES ('" + str(value) + "')")
        self.con.commit()
        print("Valor '" + value  + "' inserido no BD com sucesso!")

    def selectData(self):
        self.cur.execute('SELECT * FROM arduinoproject.environment')
        db_version = self.cur.fetchone();
        print(db_version)

    def selectAllData(self):
        self.cur.execute('SELECT * FROM arduinoproject.environment')
        rows = self.cur.fetchall()
        for row in rows:
            print row


    def closeConnecetion(self):
        self.con.close()

print("Instanciando a classe Banco...")
banco = Banco();
print("Conectando...")
banco.connection();
print("Inserindo dado no banco...")
banco.insertData('ar')
banco.insertData('agua')
banco.insertData('fogo')
print("Recuperando dados do banco...")
banco.selectAllData();
