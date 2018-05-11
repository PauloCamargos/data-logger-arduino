#!/usr/bin/python
import time
import serial

# Iniciando conexao serial
comport = serial.Serial('/dev/ttyACM0', 9600)
#comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao

PARAM_CARACTER='T'

for i in range(1,20):
# Time entre a conexao serial e o tempo para escrever (enviar algo)
    # time.sleep(0) # Entre 1.5s a 2s
#comport.write(PARAM_CARACTER)
    comport.write(PARAM_CARACTER)
    VALUE_SERIAL=comport.readline()
    print '%s. Retorno da serial: %s' % (i,VALUE_SERIAL)

# Fechando conexao serial
comport.close()
