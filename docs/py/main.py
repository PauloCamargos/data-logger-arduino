# -*- coding: utf-8 -*-
import database
import time
import serial
import os
# Iniciando conexao serial
#comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao

UMIDITY_CARACTER='U'
TEMP_CARACTER='T'
USER_ID = 1

database = database.Banco('projects','arduinoproject','postgres','banco')
database.connection()


# def startSerial():
#     # NOTE: o pyserial ja abre a porta serial qnd se inicializa deste modo
#
#     return comport
comport = serial.Serial('/dev/ttyACM0', 9600, timeout=4)

def readUnity(PARAM_CARACTER):
    # NOTE: para cada leitura ele esta abrindo e fechando a porta Serial
    # Isso não é mto otimizado
    comport.write(PARAM_CARACTER)
    VALUE_SERIAL=float(comport.readline())
    # print '%s. Retorno da serial: %s' % (PARAM_CARACTER, VALUE_SERIAL)
    return VALUE_SERIAL

# Option 1
def readTemperature():
    read_temperature = readUnity('T')
    print("A temperatura lida é: " + str(read_temperature))
    #columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures',id_user=USER_ID, id_envrmt=1, read_value=read_temperature)

# Option 2
def readUmidity():
    read_umidity = readUnity('U')
    print("A umidade lida é: " + read_umidity)
    #columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures',id_user=USER_ID, id_envrmt=1, read_value=read_temperature )


# Option 3
def readAll():
    read_temperature = readUnity('T')
    read_umidity = readUnity('U')
    print("Temperatura: " + read_temperature)
    print("Umidade: " + read_umidity)


#  Option 4
def selectLastRecord():
    pass
    # TODO: implement fetchOne query


# Option 5
def selectAllRecord():
    pass
    # TODO: implement fetchall query


def deleteLastRecord():
    pass
    # TODO: implement delete query


def deleteAllRecord():
    pass
    # TODO: impolement delete all query


def checkUser():
    USER_ID = input('Insert your user ID: ')
    return USER_ID


def menu():
    print('--------------- MENU -----------------------')
    print('0 - EXIT PROGRAM')
    print('1 - Read temperature')
    print('2 - Read umidity')
    print('3 - Read both (temp. and umid.)')
    print('4 - Visualize the last record')
    print('5 - Visualize all record')
    print('6 - Delete last record')
    print('7 - Delete all record')
    print('8 - Limpar tela')
    print('------------------------------------------\n')


checkUser()
menu()


while True:
    item = str(input("SELECT A OPTION: "))
    if item == '0':
        comport.close()
        break
    elif item == '1':
        print("Reading and inserting TEMPERATURE data into DB...")
        readTemperature();
    elif item == '2':
        print("Reading and inserting UMIDITY data into DB...")
        readUmidity();
    elif item == '3':
        print("Reading and inserting ALL data into DB...")
        readAll();
    elif item == '4':
        print("Searching  LAST record data from DB...")
        selectLastRecord();
    elif item == '5':
        print("Searching  ALL record data from DB...")
        selectAllRecord();
    elif item == '6':
        print("Deleting  LAST record data from DB...")
        deleteLastRecord();
    elif item == '7':
        print("Deletgin  ALL record data from DB...")
        deleteAllRecord();
    elif item == '8':
        os.system("clear")
        menu()

# SELECT * FROM arduinoproject.measures;
# SELECT * FROM arduinoproject.environment;
# SELECT * FROM arduinoproject.physical_quantity;
# SELECT read_value FROM arduinoproject.measures;
#
#
#
# DELETE FROM arduinoproject.environment;
# DELETE FROM arduinoproject.measures;
# DELETE FROM arduinoproject.physical_quantity;
#
# UPDATE arduinoproject.physical_quantity SET description='Humidity' WHERE id=2;
