# -*- coding: utf-8 -*-

# http://initd.org/psycopg/docs/genindex.html

import database
import time
import serial
import os

def checkUser():
    USER_ID = raw_input('>>> Insert your user ID: ')
    return USER_ID


UMIDITY_CARACTER='U'
TEMP_CARACTER='T'
USER_ID = checkUser();


database = database.Banco('projects','arduinoproject','postgres','banco')
database.connection()
comport = serial.Serial('/dev/ttyACM0', 9600, timeout=3)

def readUnity(PARAM_CARACTER):
    # NOTE: para cada leitura ele esta abrindo e fechando a porta Serial
    # Isso não é mto otimizado
    comport.write(PARAM_CARACTER)
    VALUE_SERIAL=float(comport.readline())
    # print '%s. Retorno da serial: %s' % (PARAM_CARACTER, VALUE_SERIAL)
    return VALUE_SERIAL

# Option 1
def readTemperature():
    print("Reading and inserting TEMPERATURE data into DB...")
    read_temperature = readUnity('T')
    print("The read temperature is " + str(read_temperature))
    #columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures',id_user=USER_ID, id_environment=1, id_pquantity=1, read_value=read_temperature)
    print("Success! Data inserted into database.\n")

# Option 2
def readUmidity():
    print("Reading and inserting UMIDITY data into DB...")
    read_umidity = readUnity('U')
    print("The read humidity is " + str(read_umidity))
    #columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures',id_user=USER_ID, id_environment=1,  id_pquantity=2, read_value=read_umidity)
    print("Success! Data inserted into database.\n")

# Option 3
def readAll():
    print("Reading and inserting temperature and humidity into database...")
    read_temperature = readUnity('T')
    read_umidity = readUnity('U')
    print("Success! Temperature and humidity inserted into database.\n")
    # print("Temperatura: " + read_temperature)
    # print("Umidade: " + read_umidity)

#  Option 4
def selectLastRecord(table):
    print("Fetching last record from table '" + table + "'")
    last_db_data = database.selectLastDataFrom(table)
    print(last_db_data)
    print("--------- \n")


# Option 5
def selectAllRecord(table):
    print("Fetching last record from table '" + table + "'")
    rows = database.selectAllDataFrom(table)
    for row in rows:
        print row
    print("--------- \n")

def deleteLastRecord(table):
    ans = str(raw_input("You are about to delete THE LAST record from the table '" + table +"'. ARE YOU SURE? (y/n) "))
    if ans == 'y' or ans == 'yes':
        print("Deleting last record from " + table)
        database.deleteLastRecordFrom(table)
        print("Finished operation. Table cleared.\n")
        print("----------")
    else:
        print("Canceled operation. Returning to menu...")
        print("----------")

def deleteAllRecord(table):
    ans = str(raw_input("You are about to delete ALL record from the table '" + table + "'. ARE YOU SURE? (y/n) "))
    if ans == 'y' or ans == 'yes':
        print("Deleting all records from " + table)
        database.deleteAllDataFrom(table)
        print("Finished operation. Table cleared.")
    else:
        print("Canceled operation. Returning to menu...")

def menu():
    print('\n--------------- MENU -----------------------')
    print('0 - EXIT PROGRAM')
    print('1 - Read temperature')
    print('2 - Read umidity')
    print('3 - Read both (temp. and umid.)')
    print('4 - Visualize the last record')
    print('5 - Visualize all record')
    print('6 - Delete last record')
    print('7 - Delete all record')
    print('8 - Limpar tela')
    print('--------------------------------------------\n')

menu()

while True:
    item = str(raw_input(">>> SELECT A OPTION: "))
    if item == '0' or item == 'q':
        comport.close()
        break
    elif item == '1':
        readTemperature();
    elif item == '2':
        readUmidity();
    elif item == '3':
        readAll();
    elif item == '4':
        table = str(raw_input("> Enter table name: "))
        selectLastRecord(table);
    elif item == '5':
        table = str(raw_input("> Enter table name: "))
        selectAllRecord(table);
    elif item == '6':
        table = str(raw_input("> You are about to delete data from a table. Enter table name: "))
        deleteLastRecord(table);
    elif item == '7':
        table = str(raw_input("> You are about to delete ALL data from a table. Enter table name: "))
        deleteAllRecord(table);
    elif item == '8':
        os.system('cls' if os.name == 'nt' else 'clear')
        menu()
    else:
        print("Invalid option! Choose one option from the menu above.")
