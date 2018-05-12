# -*- coding: utf-8 -*-
"""Data-Logger-Arduino Main Application
Project of the discipline of Database.
This code communicates with arduino, getting a data and inserting into a
database, it has a menu showing the options to get a new reading, insert,
read or delete.

GitHub: http://github.com/paulocamargos/data-logger-arduino

Authors
-------
    * Paulo
    * Thiago
References
----------
    1. http://initd.org/psycopg/docs/genindex.html
"""
import database
import time
import serial
import os

################
# Global Data: #
################


def checkUser():
    """Asks the user for input the USER_ID

    Returns
    -------
    int
        USER_ID inserted by the user.

    """
    USER_ID = raw_input('>>> Insert your user ID: ')
    return USER_ID


HUMIDITY_CARACTER = 'U'
TEMP_CARACTER = 'T'
USER_ID = raw_input('>>> Insert your user ID: ')
database = database.Banco('projects', 'arduinoproject',
                          'postgres', 'banco')
database.connection()
comport = serial.Serial('/dev/ttyACM0', 9600, timeout=3)

##########################
# Application Functions: #
##########################


def readUnity(PARAM_CARACTER):
    """Reads a value from the arduino sensores
    **ATENTION**: The serial port must be open before calling this function
    It sends a request to the connected arduino and waits
    for a line containing the answer to the request.
    EasterEgg: Unity is everywhere hehehe

    Parameters
    ----------
    PARAM_CARACTER : char
        The type of measure (Temperature or Humidity) must be indicated,
        by a character.

    Returns
    -------
    float
        The value returned by the arduino sensor as a float.

    Example
    -------
        >> readUnity('T') # Temperature
        25.0
        >> readUnity('U') # Humidity
        19.2

    """
    comport.write(PARAM_CARACTER)
    VALUE_SERIAL = float(comport.readline())
    # DEBUG: Uncomment here for debbuging
    # print '%s. Retorno da serial: %s' % (PARAM_CARACTER, VALUE_SERIAL)
    return VALUE_SERIAL


def readTemperature():
    """This is the option 1 in Application Menu.
    Reads the temperatura and inserts it into the database
    This function deppends of `readUnity` and of `insertDataInto`
    There also are prints showing the status of the request.

    Example
    -------
        >>> readTemperature()
        Reading and inserting TEMPERATURE data into DB...
        The read temperature is 25.0ºC.
        Success! Data inserted into database.

    """
    print("Reading and inserting TEMPERATURE data into DB...")
    read_temperature = readUnity('T')
    print("The read temperature is " + str(read_temperature) + "ºC.")
    # columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures', id_user=USER_ID,
                            id_environment=1, id_pquantity=1,
                            read_value=read_temperature)
    print("Success! Data inserted into database.\n")


def readHumidity():
    """This is the option 2 in Application Menu.
    Reads the humidity and inserts it into the database
    This function deppends of `readUnity` and of `insertDataInto`
    There also are prints showing the status of the request.

    Example
    -------
        >>> readHumidity()
        Reading and inserting HUMIDITY data into DB...
        The read humidity is 19% UR.
        Success! Data inserted into database.

    """
    print("Reading and inserting HUMIDITY data into DB...")
    read_humidity = readUnity('U')
    print("The read humidity is " + str(read_humidity))
    # columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures', id_user=USER_ID,
                            id_environment=1, id_pquantity=2,
                            read_value=read_humidity)
    print("Success! Data inserted into database.\n")


def readAll():
    """This is the option 3 in Application Menu.
    Reads the temperature and the humidity, respectivily.
    This function deppends of `readUnity`.
    There also are prints showing the status of the request.

    Example
    -------
        >>> readAll()
        Reading and inserting temperature and humidity into database...
        Success! Temperature and humidity inserted into database.

    """
    print("Reading and inserting temperature and humidity into database...")
    read_temperature = readUnity('T')
    read_humidity = readUnity('U')
    print("Success! Temperature and humidity inserted into database.\n")
    # TODO: Esta função lê os dados mas não fazer nada, ué?
    # DEBUG: Uncomment here for debbuging
    # print("Temperatura: " + read_temperature)
    # print("Umidade: " + read_humidity)


def selectLastRecord(table):
    """This is the option 4 in Application Menu.
    Reads the last row of a determined table and shows it in the terminal.

    Parameters
    ----------
    table : str
        The name of the table which will be read.

    Example
    -------
        >>> selectLastRecord('measures')
        Fetching last record from table 'measures'.

    """
    # TODO: Terminar o exemplo na documentação, confirir se é um row
    print("Fetching last record from table '" + table + "'")
    last_db_data = database.selectLastDataFrom(table)
    print(last_db_data)
    print("--------- \n")


def selectAllRecord(table):
    """This is the option 5 in Application Menu.
    Reads the all rows of a determined table and shows it in the terminal.

    Parameters
    ----------
    table : str
        The name of the table which will be read.

    Example
    -------
        >>> selectAllRecord('measures')
        Fetching all records from table 'measures'.

    """
    # TODO: Terminar o exemplo na documentação
    print("Fetching all records from table '" + table + "'")
    rows = database.selectAllDataFrom(table)
    for row in rows:
        print row
    print("--------- \n")


def deleteLastRecord(table):
    """This is the option 6 in Application Menu.
    Delets the last row of a determined table.
    Before the operation it asks the user for confimation.

    Parameters
    ----------
    table : str
        The name of the table which will have a row deleted.

    Example
    -------
        >>> deleteLastRecord('measures')
        You are about to delete THE LAST record from the table 'measures'.
        ARE YOU SURE? (y/n) yes
        Deleting last record from measures
        Finished operation. Table cleared.

    """
    ans = str(raw_input("You are about to delete THE LAST " +
                        "record from the table '" + table +
                        "'.\nARE YOU SURE? (y/n) "))
    if ans == 'y' or ans == 'yes':
        print("Deleting last record from " + table)
        database.deleteLastRecordFrom(table)
        print("Finished operation. Table cleared.\n")
        print("--------- \n")
    else:
        print("Canceled operation. Returning to menu...")
        print("--------- \n")


def deleteAllRecord(table):
    """This is the option 7 in Application Menu.
    Delets all the rows of a determined table.
    Before the operation it asks the user for confimation.

    Parameters
    ----------
    table : str
        The name of the table which will have all records deleted.

    Example
    -------
        >>> deleteAllRecord('measures')
        You are about to delete ALL records from the table 'measures'.
        ARE YOU SURE? (y/n) yes
        Deleting all records from measures
        Finished operation. Table cleared.

    """
    ans = str(raw_input("You are about to delete ALL " +
                        "records from the table '" + table +
                        "'.\nARE YOU SURE? (y/n) "))
    if ans == 'y' or ans == 'yes':
        print("Deleting all records from " + table)
        database.deleteAllDataFrom(table)
        print("Finished operation. Table cleared.")
    else:
        print("Canceled operation. Returning to menu...")


def visualizeByUser():
    """This is the option 7 in Application Menu.
    Prints in all data inserted in the Database by the current user.

    Example
    -------
        >>> visualizeByUser()
    """
    # TODO: finish docummentation
    print("Fetching all insertions by user...")
    rows = database.visualizeByUser()
    for row in rows:
        print row
    print("--------- \n")


def menu():
    """Shows a menu with the Application Options.
    This function only shows the menu, you still need to gets the user inputs.

    """
    print('\n--------------- MENU -----------------------')
    print('0 - EXIT PROGRAM')
    print('1 - Read temperature')
    print('2 - Read humidity')
    print('3 - Read both (temp. and umid.)')
    print('4 - Visualize the last record')
    print('5 - Visualize all record')
    print('6 - Delete last record')
    print('7 - Delete all record')
    print('8 - Visualize insertions by user')
    print('C - Limpar tela')
    print('--------------------------------------------\n')


def main():
    """Main Application
    """
    menu()

    while True:
        item = str(raw_input(">>> SELECT A OPTION: "))
        if item == '0' or item == 'q':
            comport.close()
            break
        elif item == '1':
            readTemperature()
        elif item == '2':
            readHumidity()
        elif item == '3':
            readAll()
        elif item == '4':
            table = str(raw_input("> Enter table name: "))
            selectLastRecord(table)
        elif item == '5':
            table = str(raw_input("> Enter table name: "))
            selectAllRecord(table)
        elif item == '6':
            table = str(raw_input("> You are about to delete data " +
                                  "from a table. Enter table name: "))
            deleteLastRecord(table)
        elif item == '7':
            table = str(raw_input("> You are about to delete ALL data " +
                                  "from a table. Enter table name: "))
            deleteAllRecord(table)
        elif item == '8':
            visualizeByUser()
        elif item == 'C' or item == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
        else:
            print("Invalid option! Choose one option from the menu above.")


if __name__ == '__main__':
    main()
