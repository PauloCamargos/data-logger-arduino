import psycopg2
import time
import serial

print ("Iniciando programa...")

class Banco:
    """Short summary.

    Parameters
    ----------
    database : type
        Description of parameter `database`.
    schema : type
        Description of parameter `schema`.
    user : type
        Description of parameter `user`.
    password : type
        Description of parameter `password`.

    Attributes
    ----------
    port : type
        Description of attribute `port`.
    host : type
        Description of attribute `host`.
    con : type
        Description of attribute `con`.
    cur : type
        Description of attribute `cur`.
    query : type
        Description of attribute `query`.
    database        schema        user        password

    """

    def __init__(self, database, schema, user, password):
        self.database = database
        self.schema = schema
        self.user = user
        self.password = password
        self.port = 5432
        self.host = "localhost"
        self.con = None
        self.cur = None
        self.query = None

    def connection(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """

        print('Conectando com o banco de dados ...')
        try:
            self.con = psycopg2.connect(database=self.database,
                                        user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)

            self.cur = self.con.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print("exception: " + error)

    def insertDataInto(self, table, **kwargs):
        """Short summary.

        Parameters
        ----------
        table : String
            Name of the table to insert.
        **kwargs : Dictionary
            Table fields and it's corresopndent values.

        Returns
        -------
        type
            Description of returned object.

        """

        fields = []
        values = []
        unknownValues = []
        self.query = "INSERT INTO " + self.schema + "." + table
        # query = "INSERT INTO arduinoproject." + table + ()"
        for key in kwargs:
            # Table's fields
            fields.append(key);
            # Table's values
            values.append(kwargs[key])
            # Placeholders
            unknownValues.append("%s")

        # Reversing to keep fields and values in the right order
        fields.reverse()
        values.reverse()
        knownFields = ", ".join(fields)
        placehold = ', '.join(unknownValues)
        if(len(values) == 1):
            self.cur.execute("INSERT INTO " + self.schema + "." + table + "(" + knownFields + ") VALUES ('" + str(values[0]) + "')")
            self.con.commit()
        else:
            knownValues = tuple(values)
            self.query = "INSERT INTO " + self.schema + "." + table + "(" + knownFields + ") VALUES(" + placehold + ")"
            print(self.query)
            print(knownValues)
            self.cur.executemany(self.query, knownValues)

        self.con.commit()
        # self.cur.close()
        # # self.cur.execute("INSERT INTO aulas.tb_log(valor) VALUES (" + str(value) + ")")
        # self.cur.execute("INSERT INTO arduinoproject.environment(description) VALUES ('" + str(value) + "')")
        # self.con.commit()
        # print("Valor '" + value  + "' inserido no BD com sucesso!")

    def selectDataFrom(self, table):
        self.cur.execute('SELECT * FROM ' + self.schema + '.' + table)
        data_output = self.cur.fetchone();
        print(data_output)

    def selectAllDataFrom(self, table):
        self.cur.execute('SELECT * FROM ' + self.schema + '.' + table)
        rows = self.cur.fetchall()
        for row in rows:
            print row

    def closeConnecetion(self):
        self.con.close()

banco = Banco('projects','arduinoproject','postgres','banco')
# Cria conexao:
banco.connection();
banco.insertDataInto(table='environment', description='soil')
banco.selectAllDataFrom(table='environment')
