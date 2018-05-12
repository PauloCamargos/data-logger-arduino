# -*- coding: utf-8 -*-

import psycopg2
import time
import serial

"""
USED SQL:
 - INSERT
 - CREATE
 - DELETE
 - UPDATE
 - COUNT
"""

def main():
    banco = Banco('projects','arduinoproject','postgres','banco')
    # Cria conexao:
    banco.connection();
    # banco.insertDataInto(table='physical_quantity', description='Temperature', unity='°C')
    # banco.insertDataInto(table='physical_quantity', description='Umidty', unity='%')
    # banco.insertDataInto(table='environment', description='soil')
    # banco.insertDataInto(table='environment', description='water')
    # banco.insertDataInto(table='environment', description='air')
    # banco.deleteDataFrom(table='physical_quantity', condition='id', condition_value='4')
    # banco.selectAllDataFrom(table='users')
    # banco.updateData(table='physical_quantity', condition='id', condition_value= '7', description='tensao', unity='volts')

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
            print("exception: " + error)

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

        # Converting known values in tuple
        knownValues = tuple(values)
        self.query = "INSERT INTO " + self.schema + "." + table + "(" + knownFields + ") VALUES(" + placehold + ")"
        print(self.query)
        print(knownValues)

        self.cur.execute(self.query, knownValues)
        self.con.commit()

    def updateDataFrom(self, table, condition, condition_value, **parameters ):
        """Updates data of a table using the parameters as fields and it's
        values as data to be updated.

        Parameters
        ----------
        table : String
            Table which the data will be updated.
        condition : String
            Field record where data will be updated.
        condition_value : String
            Value record where data will be updated.
        **kwargs : String
            Fields and values to be updated in the table. Use the template
            fieldName='value' to pass the columns and values. Unlimited number of
            parameters allowed here.

        Returns
        -------
        void
        """

        fields_values= " "
        values = []

        self.query = "UPDATE " + self.schema + "." + table

        for key in parameters:
            # Table's fields
            fields_values += str(key) + "=%s,"
            # Table's values
            values.append(parameters[key])

        values.append(condition_value)
        fields_values = fields_values[:-1]
        knownValues = tuple(values)

        self.query += " SET" + fields_values  + " WHERE " +condition+"=%s"

        print(self.query)
        print(knownValues)

        try:
            self.cur.execute(self.query, knownValues)
            self.con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def selectDataFrom(self, table):
        self.cur.execute("SELECT * FROM " + self.schema + "." + table + ";")
        one_row_data = self.cur.fetchone()
        return row

    def selectAllDataFrom(self, table):
        self.query = "SELECT * FROM " + self.schema + "."  + table + ";"
        self.cur.execute(self.query)
        rows = self.cur.fetchall()
        return rows

    def deleteLastRecordFrom(self, table):
        self.cur.execute("SELECT MAX(id) FROM " + self.schema + "."  + table)
        id_last_record = self.cur.fetchone();
        self.query = "DELETE FROM " + self.schema + "."  + table + " WHERE id=%s"
        data = (id_last_record,)
        self.cur.execute(self.query, data)
        self.con.commit()
        print(self.query)

    def deleteAllDataFrom(self, table):
        self.query = "DELETE FROM " + self.schema + "."  + table;
        self.cur.execute(self.query)
        self.con.commit()


    def closeConnecetion(self):
        """Closes the connection.

        Returns
        -------
        void
        """

        self.con.close()


if __name__ == "__main__":
    main()
