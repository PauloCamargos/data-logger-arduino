# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogfernandes
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import serial
import serial.tools.list_ports as serial_tools
from time import sleep
from ctypes import c_short
import sys
if sys.version_info.major == 2:
    from Queue import Queue
else:
    from queue import Queue
# ------------------------------------------------------------------------------


class ArduinoConstants:
    """
    Save here the constants with the arduino communication.
    CONSTANTS:
    ---------
    CMD_LIGAR_VENTILADOR : Turns on a cooler.
    CMD_DESLIGAR_VENTILADOR : Turns off the cooler.
    CMD_LIGAR_IRRIGADOR : Turns on a hidraulic valve.
    CMD_DESLIGAR_IRRIGADOR : Turns off the hidraulic valve.
    CMD_LER_DADOS : Requests the data from the sensors.
                    Arduino answer are described in README.md
    COMM_UMIDADE : Indicates a umidity measure.
    COMM_TEMPERATURA : Indicates a temperature measure.
    COMM_END : Every packet from arduino to computer has this byte at the end.
    """
    # Commands
    CMD_LIGAR_VENTILADOR    = 'T'
    CMD_DESLIGAR_VENTILADOR = 't'
    CMD_LIGAR_IRRIGADOR     = 'U'
    CMD_DESLIGAR_IRRIGADOR  =  'u'
    CMD_LER_DADOS           = 'R'
    # Communication
    COMM_UMIDADE        = 'U'
    COMM_TEMPERATURA    = 'T'
    COMM_END            = '\n'
    # For finding the serial port automatically
    MANUFACTURER = 'Arduino (www.arduino.cc)'

class ArduinoHandler:
    """
    This class handles all the communication with a arduino board.

    It has a serialPort Object, a Buffer and a Thread for acquisition.
    Parameters
    ----------
    port_name : String containing the name of the serial port.
                Examples are: 'COM3', 'COM4', '/dev/ttyACM0'
                If it's not set, a compatible port will be searched.
    baudrate : The speed of the communication, in bits per second.
                As the communications is an asynchronous one, it should be
                set here the same of is in the arduino code.
    Examples
    --------
    See the code of the test function in this file for two command line examples.
    """
    def __init__(self, port_name=None, baudrate=9600):
        if port_name is None:
            port_name = ArduinoHandler.get_arduino_serial_port()
        self.serial_tools_obj = [s for s in serial_tools.comports() if s.device == port_name][0]
        self.serialPort = serial.Serial()
        self.serialPort.port = port_name
        self.serialPort.baudrate = baudrate

    def open(self):
        """
        If it is not already open, it will open the serial port and flush its buffers.
        """
        if not self.serialPort.isOpen():
            self.serialPort.open()
            self.serialPort.flushInput()
            self.serialPort.flushOutput()

    def close(self):
        """
        If the serial port is open, this method will try to close it.
        """
        if self.serialPort.isOpen():
            self.serialPort.close()

    @staticmethod
    def get_arduino_serial_port():
        """
        Tries to found a serial port compatible.

        If there is only one serial port available, return this one.

        Otherwise it will verify the manufacturer of all serial ports
        and compares with the manufacturer defined in the ArduinoConstants.
        This method will return the first match.

        If no one has found, it will return a empty string.
        :return: Serial Port String
        """
        serial_ports = serial_tools.comports()
        if len(serial_ports) == 0:
            return ""
        if len(serial_ports) == 1:
            return serial_ports[0].device
        for serial_port_found in serial_ports:
            if serial_port_found.manufacturer == ArduinoConstants.MANUFACTURER:
                return serial_port_found.device
        return ""
    def set_fan_state(self, new_state):
        if new_state:
            self.serialPort.write(ArduinoConstants.CMD_LIGAR_VENTILADOR)
        else:
            self.serialPort.write(ArduinoConstants.CMD_DESLIGAR_VENTILADOR)

    def set_irrigator_state(self, new_state):
        if new_state:
            self.serialPort.write(ArduinoConstants.CMD_LIGAR_IRRIGADOR)
        else:
            self.serialPort.write(ArduinoConstants.CMD_DESLIGAR_IRRIGADOR)

    def get_readings_dict(self):
        self.serialPort.write(ArduinoConstants.CMD_LER_DADOS)

        # TODO: Se for usar o methodo read_all, colocar um timer.sleep
        # com o tempo maximo de resposta do sensor
        sleep(0.5) # Aguarda o arduino responder

        arduino_msg = self.serialPort.read_all()
        arduino_msg1 = arduino_msg.split()[0]
        arduino_msg2 = arduino_msg.split()[1]

        #TODO: Usar estes comandos e tirar o time.sleep()
        # Setar timeout da conexão para o tempo maximo de resposta do sensor
        # arduino_msg1 = self.serialPort.readline()
        # arduino_msg2 = self.serialPort.readline()

        leituras = {}

        msg1_type = arduino_msg1[0]
        msg1_info = float(arduino_msg1[1:])
        msg2_type = arduino_msg2[0]
        msg2_info = float(arduino_msg2[1:])

        if msg1_type == ArduinoConstants.COMM_TEMPERATURA:
            leituras['Temperatura'] = msg1_info
            leituras['Umidade'] = msg2_info
        elif msg1_type == ArduinoConstants.COMM_UMIDADE:
            leituras['Umidade'] = msg1_info
            leituras['Temperatura'] = msg2_info

        return leituras

    def __str__(self):
        return "ArduinoHandlerObject" +\
              "\n\tSerialPort: " + str(self.serial_tools_obj.device) +\
              "\n\tDescription: " + str(self.serial_tools_obj.description) +\
              "\n\tOpen: " + str(self.serialPort.isOpen())


def test():
    my_arduino_handler = ArduinoHandler(port_name='/dev/ttyUSB0')

    def show_status():
        print(my_arduino_handler)

    while True:
        print('-------------------------------')
        print(my_arduino_handler)
        print('-------------------------------')
        print('Menu')
        print('-------------------------------')
        print('q - Quit')
        print('-------------------------------')
        print('o - open() ')
        print('c - close()')
        print('r - readall()')
        print('-------------------------------')
        print(ArduinoConstants.CMD_LIGAR_VENTILADOR, ' - Ligar Ventilador')
        print(ArduinoConstants.CMD_DESLIGAR_VENTILADOR, ' - Desligar Ventilador')
        print(ArduinoConstants.CMD_LIGAR_IRRIGADOR, ' - Ligar Irrigador')
        print(ArduinoConstants.CMD_DESLIGAR_IRRIGADOR, ' - Desligar Irrigador')
        print('-------------------------------')
        print(ArduinoConstants.CMD_LER_DADOS, ' - Ler Dados dos Sensores')
        print('-------------------------------')

        if sys.version_info.major == 2:
            str_key = raw_input()
        else:
            str_key = input()

        if 'q' in str_key:
            my_arduino_handler.close()
            break
        elif 'o' in str_key:
            my_arduino_handler.open()
        elif 'c' in str_key:
            my_arduino_handler.close()
        elif 'r' in str_key:
            print(my_arduino_handler.serialPort.read_all())
        elif ArduinoConstants.CMD_LIGAR_VENTILADOR in str_key:
            my_arduino_handler.set_fan_state(True)
        elif ArduinoConstants.CMD_DESLIGAR_VENTILADOR in str_key:
            my_arduino_handler.set_fan_state(False)
        elif ArduinoConstants.CMD_LIGAR_IRRIGADOR in str_key:
            my_arduino_handler.set_irrigator_state(True)
        elif ArduinoConstants.CMD_DESLIGAR_IRRIGADOR in str_key:
            my_arduino_handler.set_irrigator_state(False)
        elif ArduinoConstants.CMD_LER_DADOS in str_key:
            print(my_arduino_handler.get_readings_dict())

def main():
    test()

if __name__ == '__main__':
    main()
