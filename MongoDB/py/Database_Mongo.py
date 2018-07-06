from pymongo import *
from bson.objectid import ObjectId
import serial  # serial communication
import time  # time.sleep(int)
import os  # os.system('clear')
import math
import serial.tools.list_ports
import pprint

################
# Global Data: #
################
HUMIDITY_CHARACTER = 'A'.encode()
TEMP_CHARACTER = 'T'.encode()
SOIL_HUMIDITY_CHARACTER = 'S'.encode()

client = MongoClient('localhost', 27017)  # Iniciando a conexão com o banco
db = client.datalogger  # Acessando a Collection "datalogger"

port_name = serial.tools.list_ports.comports()[0].device
print(port_name)
comport = serial.Serial(port_name, 9600, timeout=3)

# Getting collections
environment_coll = db.environments
pquantity_coll = db.physical_quantity
measures_coll = db.measures
users_coll = db.users

def checkUser():
    """Asks the user for input the USER_ID

        Returns
        -------
        tuple
            USER_ID and USER_FULLNAME.

        """
    username_value = str(input('>>> Insert your username: '))

    user = users_coll.find_one(
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


def readUnity(PARAM_CARACTER):
    """        Reads a value from the arduino sensors
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
    time.sleep(1.8)
    VALUE_SERIAL = float(comport.readline())
    # Case read value is nan
    if math.isnan(VALUE_SERIAL):
        VALUE_SERIAL = -1
    # DEBUG: Uncomment here for debbuging
    # print '%s. Retorno da serial: %s' % (PARAM_CARACTER, VALUE_SERIAL)
    return VALUE_SERIAL



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
    id_environment = environment_coll.find_one(
        {'description': 'Ar'}, {'_id': 1}
    )
    id_environment = id_environment.get('_id')

    id_pquantity = pquantity_coll.find_one(
        {'type': 'Temperatura', 'unity': '°C'}, {'_id': 1}
    )
    id_pquantity = id_pquantity.get('_id')

    print("Reading and inserting TEMPERATURE data into DB...")
    read_temperature = readUnity(TEMP_CHARACTER)
    if read_temperature != -1:
        print("The read temperature is " + str(read_temperature) + "ºC.")
        # columns: id_user, id_envrmt, read_value
        measures_coll.insert_one(
            {
            'id_user': user_id,
            'id_environment': id_environment,
            'id_pquantity': id_pquantity,
            'read_value': read_temperature
            }
        )
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

    id_environment = environment_coll.find_one({'description': 'Ar'}, {'_id': 1})
    id_pquantity = pquantity_coll.find_one({'type': 'Umidade'}, {'_id': 1})

    id_environment = id_environment.get('_id')
    id_pquantity = id_pquantity.get('_id')

    print("Reading and inserting HUMIDITY data into DB...")
    read_humidity = readUnity(HUMIDITY_CHARACTER)
    if read_humidity != -1:
        print("The read AIR humidity is " + str(read_humidity) + "%")
        # columns: id_user, id_envrmt, read_value
        measures = db.measures
        measures_coll.insert_one({'id_user': user_id,
                                'id_environment': id_environment,
                                'id_pquantity': id_pquantity,
                                'read_value': read_humidity}
                                )
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

    id_environment = environment_coll.find_one({'description': 'Solo'}, {'_id': 1})
    id_pquantity = pquantity_coll.find_one({'type': 'Umidade'}, {'_id': 1})

    id_environment = id_environment.get('_id')
    id_pquantity = id_pquantity.get('_id')

    print("Reading and inserting HUMIDITY data into DB...")
    read_humidity = readUnity(SOIL_HUMIDITY_CHARACTER)
    if read_humidity != -1:
        print("The read humidity of the soil is " + str(read_humidity) + "%")
        # columns: id_user, id_envrmt, read_value
        measures_coll.insert_one(
            {
                'id_user': user_id,
                'id_environment': id_environment,
                'id_pquantity': id_pquantity,
                'read_value': read_humidity
             }
         )
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


def selectLastRecord(collection):
    """This is the option 4 in Application Menu.
    Reads the last row of a determined collection and shows it in the terminal.

    Parameters
    ----------
    collection : str
        The name of the collection which will be read.

    Example
    -------
        #>>> selectLastRecord('measures')
        Fetching last record from collection 'measures'.

    """

    collection_name = collection
    collection = db[collection_name]
    last_db_data = collection.find().sort('_id', -1).limit(1)

    # if collection == 'measures':
    #     measures = db.measures
    #     last_db_data = measures.find().sort('_id', -1).limit(1)
    # elif collection == 'environment':
    #     environment = db.environment
    #     last_db_data = environment.find().sort('_id', -1).limit(1)
    # elif collection == 'physical_quantity':
    #     p_quantity = db.physical_quantity
    #     last_db_data = p_quantity.find().sort('_id', -1).limit(1)

    # print("Fetching last record from collection '" + collection + "'")

    for i in last_db_data:
        print(i)
    print("--------- \n")


def selectAllRecord(collection):
    """This is the option 5 in Application Menu.
    Reads all the rows of a determined collection and shows it in the terminal.

    Parameters
    ----------
    collection : str
        The name of the collection which will be read.

    Example
    -------
       # >>> selectAllRecord('measures')
        Fetching all records from collection 'measures'...

    """
    # TODO: Terminar o exemplo na documentação

    collection_name = collection
    collection = db[collection_name]
    documents = collection.find()

    # if collection == 'measures':
    #     measures = db.measures
    #     documents = measures.find()
    # elif collection == 'environment':
    #     environment = db.environment
    #     documents = environment.find()
    # elif collection == 'physical_quantity':
    #     p_quantity = db.physical_quantity
    #     documents = p_quantity.find()

    # print("Fetching all records from collection '" + collection + "'")

    if documents:
        for document in documents:
            print(document)
    else:
        print("No data found!")
    print("--------- \n")


def deleteLastRecord(collection):
    """This is the option 6 in Application Menu.
    Delets the last row of a determined collection.
    Before the operation it asks the user for confimation.

    Parameters
    ----------
    collection : str
        The name of the collection which will have a row deleted.

    Example
    -------
        #>>> deleteLastRecord('measures')
        You are about to delete THE LAST record from the collection 'measures'.
        ARE YOU SURE? (y/n) yes
        Deleting last record from measures
        Finished operation. Collection cleared.

    """

    collection_name = collection
    collection = db[collection_name]
    collection.find_one_and_delete({}, sort=[('_id', -1)])

    # if collection == 'measures':
    #     measures = db.measures
    #     measures.find_one_and_delete({}, sort=[('_id', -1)])
    # elif collection == 'environment':
    #     environment = db.environment
    #     environment.find_one_and_delete({}, sort=[('_id', -1)])
    # elif collection == 'physical_quantity':
    #     p_quantity = db.physical_quantity
    #     p_quantity.find_one_and_delete({}, sort=[('_id', -1)])

    print("Deleting last record from " + collection_name)
    print("Finished operation. Collection cleared.\n")
    print("--------- \n")


def deleteAllRecord(collection):
    """This is the option 7 in Application Menu.
    Delets all the rows of a determined collection.
    Before the operation it asks the user for confimation.

    Parameters
    ----------
    collection : str
        The name of the collection which will have all records deleted.

    Example
    -------
        #>>> deleteAllRecord('measures')
        You are about to delete ALL records from the collection 'measures'.
        ARE YOU SURE? (y/n) yes
        Deleting all records from measures
        Finished operation. Collection cleared.

    """
    collection_name = collection
    collection = db[collection_name]
    collection.delete_many({})

    print("Deleting all records from " + collection_name)
    print("Finished operation. Collection cleared.")
    print("--------- \n")

def visualizeByUser():
    print("Vai filhão!")
    pipeline = [
    {
        '$lookup': {
            'from': 'users',
            'localField': 'id_user',
            'foreignField': '_id',
            'as': 'user'

        }
    },
    {
        '$unwind': '$user'
    },
    {
        "$lookup": {
            "from": "environments",
            "localField": "id_environment",
            "foreignField": "_id",
            "as": "environment"
        }
    },
    {
        "$unwind": "$environment"
    },
    {
        "$lookup": {
            "from": "physical_quantity",
            "localField": "id_pquantity",
            "foreignField": "_id",
            "as": "pquantity"
        }
    },
        {
            "$unwind": "$pquantity"
        }
    ]

    # pprint.pprint(collect_result)
    for doc in (measures_coll.aggregate(pipeline)):

        pprint.pprint(
        str(doc.get("user").get("fullname")) + " | " +
        str(doc.get("pquantity").get("type")) + " | " +
        str(doc.get("environment").get("description")) + " | " +
        str(doc.get("read_value")) + 
        str(doc.get("pquantity").get("unity")))


def closeConnecetion(self):
    """Closes the connection.

    Returns
    -------
    void
    """
    client.close()


def menu():
    """Shows a menu with the Application Options.
    This function only shows the menu, you still need to gets the user inputs.

    """
    print('\n----------------------------- MENU ------------------------------')
    print('0 - EXIT PROGRAM                     |    10 - Create user')
    print('1 - Read temperature                 |    11 - Check users info')
    print('2 - Read air humidity                |    12 - Update user infos')
    print('3 - Read soil humidity               |    13 - Remove user')
    print('4 - Visualize the last record        |    14 - Read both (temp. and umid.) ')
    print('5 - Visualize all record             |    15 - Delete record from collection by id')
    print('6 - Delete last record               |    16 - *')
    print('7 - Delete all record                |    17 - *')
    print('8 - Visualize insertions by user     |    18 - *')
    print('C - CLEAR SCREEN                     |    19 - *')
    print('-----------------------------------------------------------------\n')
    # * to be implemented


def main():
    """Main Application
    """
    menu()

    while True:
        item = str(input(">>> SELECT AN OPTION: "))
        if item == '0' or item == 'q':
            comport.close()
            break
        elif item == '1':
            readTemperature()
        elif item == '2':
            readAirHumidity()
        elif item == '3':
            readSoilHumidity()
        elif item == '4':
            collection = str(input("> Enter collection name: "))
            selectLastRecord(collection)
        elif item == '5':
            collection = str(input("> Enter collection name: "))
            selectAllRecord(collection)

        elif item == '6':
            ans = str(input("You are about to delete the LAST " +
                            "record of a collection.\nARE YOU SURE? (y/n) "))
            if ans.lower() == 'y' or ans.lower() == 'yes':
                collection = str(input("> Enter the collection's name: "))
                deleteLastRecord(collection)
            else:
                print("Operation aborted. Returning to menu...")
                print("--------- \n")

        elif item == '7':
            ans = str(input("> You are about to delete the ALL data " +
                            "of a collection. \nARE YOU SURE? (yes/no) "))

            if ans.lower() == 'y' or ans.lower() == 'yes':
                collection = str(input("> Enter the collection's name: "))
                deleteAllRecord(collection)
            else:
                print("Operation aborted. Returning to menu...")
                print("--------- \n")

        elif item == '8':
           visualizeByUser()

        elif item == 'C' or item == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()

        elif item == '10':
            # TODO: Check possibility of dividing this main.py in classes
            print("---------------- CREATE USER -----------")
            fullname = str(input("Enter user's full name: "))
            username = str(input("Enter user's username: "))
            status = str(input("Enter user's status: "))
            password = str(input("Enter user's password: "))
            users = db.users
            users_coll.insert_one({'username': username,
                                'fullname': fullname,
                                'status': status,
                                'password': password})
            print("User created with success!")
            print("--------- \n")

        elif item == '11':
            print("\n---------------- USERs INFOs-----------")
            print("Fetching all records from collection 'users'...")
            users = db.users
            rows = users_coll.find()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No data found!")
            print("--------- \n")

        elif item == '12':
            print("\n-------------- UPDATE USER ---------")
            username = str(input("> Type the username of the user whose data will be updated: "))
            field = str(input("> Update which field(s)? Ex.: 'fullname', 'status', 'password': "
                              "(The ' ' signs are required) ") )
            field = field.split(",")
            values = str(input("> Which values? (same order): "))
            values = values.split(",")
            fv_dictio = dict(zip(field, values))
            users = db.users
            users_coll.update_one({'username': username}, {'$set': fv_dictio})
            print("User updated with success!")
            print("--------- \n")

        elif item == '13':
            print("\n-------------- REMOVE USER ---------")
            usrname = str(input("> Type the username of the user to be removed: "))
            users = db.users
            users_coll.find_one_and_delete({'username': usrname})
            print("User deleted with success!")
            print("--------- \n")

        elif item == '14':
            readAll()

        elif item == '15':
            print("\n-------------- DELETE RECORD FROM TABLE BY ID----------")
            collection_name = str(input("> Type the collection's name from which the record will be removed: "))
            collection = db[collection_name]
            id_record = str(input("> Type the id of the record to be removed: "))
            collection.delete_one({'_id': ObjectId(id_record) })
            # database.deleteDataFrom(collection=collection, condition='id', condition_value=id_record)
            print("Data deleted with success!")
            print("--------- \n")

        else:
            print("Invalid option! Choose one option from the menu above.\n")


if __name__ == '__main__':
    main()
