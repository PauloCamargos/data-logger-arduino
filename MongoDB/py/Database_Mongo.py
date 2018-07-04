from pymongo import *
import serial  # serial communication
import time #time.sleep(int)
import os  # os.system('clear')
import math
#import serial.tools.list_ports

################
# Global Data: #
################
HUMIDITY_CHARACTER = 'A'
TEMP_CHARACTER = 'T'
SOIL_HUMIDITY_CHARACTER = 'S'

client = MongoClient('localhost', 27017)  # Iniciando a conexão com o banco
db = client.datalogger  # Acessando a Collection "datalogger"

#port_name = serial.tools.list_ports.comports()[0].device
#print(port_name)
#comport = serial.Serial(port_name, 9600, timeout=3)


def checkUser():

    """Asks the user for input the USER_ID

        Returns
        -------
        tuple
            USER_ID and USER_FULLNAME.

        """
    username_value = str(input('>>> Insert your username: '))
    users = db.users
    user = users.find_one(
        {'username': username_value},
        {'_id': 1, 'usr_fullname': 1}
    )

    return user


user_data = checkUser()
user_id = user_data.get('_id')
user_fullname = user_data.get('usr_fullname')


##########################
# Application Functions: #
##########################

"""
def readUnity(PARAM_CARACTER):
        Reads a value from the arduino sensors
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

    
    comport.write(PARAM_CARACTER)
    time.sleep(1.8)
    VALUE_SERIAL = float(comport.readline())
    # Case read value is nan
    if math.isnan(VALUE_SERIAL):
        VALUE_SERIAL = -1
    # DEBUG: Uncomment here for debbuging
    # print '%s. Retorno da serial: %s' % (PARAM_CARACTER, VALUE_SERIAL)
    return VALUE_SERIAL
"""

def readTemperature():
    """This is the option 1 in Application Menu.
    Reads the temperatura and inserts it into the database
    This function deppends of `readUnity` and of `insertDataInto`
    There are also prints showing the status of the request.

    Example
    -------
    #   >>> readTemperature()
        Reading and inserting TEMPERATURE data into DB...
        The read temperature is 25.0ºC.
        Success! Data inserted into database.
    """
    
    print("Reading and inserting TEMPERATURE data into DB...")
    read_temperature = readUnity(TEMP_CHARACTER)

    if read_temperature != -1:
        print("The read temperature is " + str(read_temperature) + "ºC.")
        # columns: id_user, id_envrmt, read_value
        measures = db.measures
        measures.insert_one({'id_user': user_id, 'id_environment': 3, 'id_pquantity': 1,
                                      'read_value': read_temperature})
        print("Success! Data inserted into database.\n")
    else:
        print("Failed to read temperature. Try again in 5 seconds.")


def readAirHumidity():
    """This is the option 2 in Application Menu.
    Reads the humidity and inserts it into the database
    This function deppends of `readUnity` and of `insertDataInto`
    There also are prints showing the status of the request.

    Example
    -------
       #>>> readAirHumidity()
        Reading and inserting HUMIDITY data into DB...
        The read humidity is 19% UR.
        Success! Data inserted into database.

    """
    print("Reading and inserting HUMIDITY data into DB...")
    read_humidity = readUnity(HUMIDITY_CHARACTER)
    if read_humidity != -1:
        print("The read AIR humidity is " + str(read_humidity) + "%")
        # columns: id_user, id_envrmt, read_value
        measures = db.measures
        measures.insert_one({'id_user': user_id, 'id_environment': 3, 'id_pquantity': 2,
                                      'read_value': read_humidity})
        print("Success! Data inserted into database.\n")
    else:
        print("Failed to read temperature. Try again in 5 seconds.")


def readSoilHumidity():
    """This is the option 3 in Application Menu.
    Reads the humidity and inserts it into the database
    This function deppends of `readUnity` and of `insertDataInto`
    There also are prints showing the status of the request.

    Example
    -------
        >>> readAirHumidity()
        Reading and inserting HUMIDITY data into DB...
        The read humidity is 19% UR.
        Success! Data inserted into database.

    """
    print("Reading and inserting HUMIDITY data into DB...")
    read_humidity = readUnity(SOIL_HUMIDITY_CHARACTER)
    if read_humidity != -1:
        print("The read humidity of the soil is " + str(read_humidity) + "%")
        # columns: id_user, id_envrmt, read_value
        measures = db.measures
        measures.insert_one({'id_user': user_id, 'id_environment': 1, 'id_pquantity': 2,
                             'read_value': read_humidity})
        print("Success! Data inserted into database.\n")
    else:
        print("Failed to read temperature. Try again in 5 seconds.")


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
    readTemperature()
    readAirHumidity()
    readSoilHumidity()
    print("Success! Temperature and humidity inserted into database.\n")
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
        #>>> selectLastRecord('measures')
        Fetching last record from table 'measures'.

    """

    if table == 'measures':
        measures = db.measures
        last_db_data = measures.find().sort('_id', -1).limit(1)
    elif table == 'environment':
        environment = db.environment
        last_db_data = environment.find().sort('_id', -1).limit(1)
    elif table == 'physical_quantity':
        p_quantity = db.physical_quantity
        last_db_data = p_quantity.find().sort('_id', -1).limit(1)


    print("Fetching last record from table '" + table + "'")

    for i in last_db_data:
        print(i)
    print("--------- \n")


def selectAllRecord(table):
    """This is the option 5 in Application Menu.
    Reads all the rows of a determined table and shows it in the terminal.

    Parameters
    ----------
    table : str
        The name of the table which will be read.

    Example
    -------
       # >>> selectAllRecord('measures')
        Fetching all records from table 'measures'...

    """
    # TODO: Terminar o exemplo na documentação

    if table == 'measures':
        measures = db.measures
        documents = measures.find()
    elif table == 'environment':
        environment = db.environment
        documents = environment.find()
    elif table == 'physical_quantity':
        p_quantity = db.physical_quantity
        documents = p_quantity.find()

    print("Fetching all records from table '" + table + "'")

    if documents:
        for document in documents:
            print(document)
    else:
        print("No data found!")
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
        #>>> deleteLastRecord('measures')
        You are about to delete THE LAST record from the table 'measures'.
        ARE YOU SURE? (y/n) yes
        Deleting last record from measures
        Finished operation. Table cleared.

    """

    if table == 'measures':
        measures = db.measures
        measures.find_one_and_delete({}, sort=[('_id', -1)])
    elif table == 'environment':
        environment = db.environment
        environment.find_one_and_delete({}, sort=[('_id', -1)])
    elif table == 'physical_quantity':
        p_quantity = db.physical_quantity
        p_quantity.find_one_and_delete({}, sort=[('_id', -1)])


    print("Deleting last record from " + table)
    print("Finished operation. Table cleared.\n")
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
        #>>> deleteAllRecord('measures')
        You are about to delete ALL records from the table 'measures'.
        ARE YOU SURE? (y/n) yes
        Deleting all records from measures
        Finished operation. Table cleared.

    """

    if table == 'measures':
        measures = db.measures
        measures.delete_many({})
    elif table == 'environment':
        environment = db.environment
        environment.delete_many({})
    elif table == 'physical_quantity':
        p_quantity = db.physical_quantity
        p_quantity.delete_many({})

    print("Deleting all records from " + table)
    print("Finished operation. Table cleared.")
    print("--------- \n")


def closeConnecetion(self):
    """Closes the connection.

    Returns
    -------
    void
    """
    client.close()


deleteAllRecord('measures')