import psycopg2
import time
import serial


def main():
    banco = Banco('projects','arduinoproject','postgres','banco')
    # Cria conexao:
    banco.connection();
    banco.insertDataInto(table='environment', description='soil')
    banco.selectAllDataFrom(table='environment')


class Banco:
    """Database class. Use this class to create connection e execute CRUD
    commands on a database.

    Parameters
    ----------
    database : String
        Database name.
    schema : type
        Schema which the tables are stored.
    user : String
        User's username to access to database.
    password : type
        User's password to access the database.
    port : int
        Port number which the database uses.
    host : type
        Database host address.
    """

    def __init__(self, database, schema, user, password, port=5432, host='localhost'):
        self.database = database
        self.schema = schema
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.con = None
        self.cur = None
        self.query = None

    def connection(self):
        """Creates connection with the database using the specified parameter at
        the class constructor.

        Returns
        -------
        void
        """

        try:
            self.con = psycopg2.connect(database=self.database,
                                        user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)

            self.cur = self.con.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print("exception: " + str(error))

    def insertDataInto(self, table, **kwargs):
        """Inserts data into a table using the parameters as fields and it's
        values as data to be inserted.

        Parameters
        ----------
        table : String
            Table which the data will be inserted.
        **kwargs : String
            Fields and values to be inserted in the table. Use the template
            fieldName='value' to pass the columns and values. Ilimited number of
            parameters allowed here.

        Returns
        -------
        void
        """

        fields = []
        values = []
        unknownValues = []
        self.query = "INSERT INTO " + self.schema + "." + table

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

        # Converting the lists in string
        knownFields = ", ".join(fields)
        placehold = ', '.join(unknownValues)

        if(len(values) == 1): # Case only one value is inserted
            self.cur.execute("INSERT INTO " + self.schema + "." + table + "(" + knownFields + ") VALUES ('" + str(values[0]) + "')")
        else:
            knownValues = tuple(values)
            self.query = "INSERT INTO " + self.schema + "." + table + "(" + knownFields + ") VALUES(" + placehold + ")"
            print(self.query)
            print(knownValues)
            self.cur.executemany(self.query, knownValues)

        self.con.commit()

    def selectDataFrom(self, table):
        """Selects one row data from the specified table.

        Parameters
        ----------
        table : String
            Table name which data will be fetched.

        Returns
        -------
        String
            Value fetched from the query.
        """

        self.cur.execute('SELECT * FROM ' + self.schema + '.' + table)
        data_output = self.cur.fetchone();
        print(data_output)

        return data_output

    def selectAllDataFrom(self, table):
        """Selects all data from the specified table.

        Parameters
        ----------
        table : String
            Table name which data will be fetched.

        Returns
        -------
        String tuple
            Values fetched from the query. Each tuple represents a row.
        """
        self.cur.execute('SELECT * FROM ' + self.schema + '.' + table)
        rows = self.cur.fetchall()
        for row in rows:
            print row

        return rows

    def closeConnecetion(self):
        """Closes the connection.

        Returns
        -------
        void
        """

        self.con.close()

    def updataDataFrom(self, table):
        pass
        # TODO: Create update method

    def deleteDataFrom(self, table):
        pass
        # TODO: Create delet method


if __name__ == "__main__":
    main()
