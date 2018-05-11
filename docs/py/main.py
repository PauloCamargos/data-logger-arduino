import database
import time
import serial
#!-*- conding: utf8 -*-
# coding: utf-8
# Iniciando conexao serial
#comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao

UMIDITY_CARACTER='U'
TEMP_CARACTER='T'
USER_ID = 1

database = database.Banco('projects','arduinoproject','postgres','banco')
database.connection()


def startSerial():
    comport = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    return comport

def readUnity(PARAM_CARACTER):
    comport = startConnection();
    comport.write(PARAM_CARACTER)
    VALUE_SERIAL=comport.readline()
    print '%s. Retorno da serial: %s' % (PARAM_CARACTER, VALUE_SERIAL)
    comport.close()
    return VALUE_SERIAL

# Option 1
def readTemperature():
    read_temperature = readUnity('T')
    #columns: id_user, id_envrmt, read_value
    database.insertDataInto(table='measures',id_user=id_loggedUser,read_value=read_temperature )

# Option 2
def readUmidity():
    readUnity('U')

# Option 3
def readAll():
    temperature = readUnity('T')
    umidity = readUnity('U')
    # TODO: implement database queries

#  Option 4
def selectOneRecord():
    # TODO: implement fetchOne query


# Option 5
def selectAllRecord():
    # TODO: implement fetchall query

def deleteLastRecord():
    # TODO: implement delete query

def deleteAllRecord():
    # TODO: impolement delete all query

def checkUser():
    USER_ID = input('Insert your user ID:')
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
    print('------------------------------------------\n')

while True:
    print("------------ BEGINNING PROGRAM -------------")
    checkUser()
    menu()
    item = str(input("SELECT A OPTION: "))

    switch
    if item == '0':
        break
    elif
