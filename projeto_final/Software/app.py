# -*- coding: utf-8 -*-
"""Example NumPy style docstrings.
This module demonstrates documentation as specified by the `NumPy
Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
are created with a section header followed by an underline of equal length.
Example
-------
Examples can be given using either the ``Example`` or ``Examples``
sections. Sections support any reStructuredText formatting, including
literal blocks::
    $ python example_numpy.py
Section breaks are created with two blank lines. Section breaks are also
implicitly created anytime a new section starts. Section bodies *may* be
indented:
Notes
-----
    This is an example of an indented section. It's like any other section,
    but the body is indented to help it stand out from surrounding text.
If a section is indented, then a section break is created by
resuming unindented text.
Attributes
----------
module_level_variable1 : int
    Module level variables may be documented in either the ``Attributes``
    section of the module docstring, or in an inline docstring immediately
    following the variable.
    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.
.. _NumPy Documentation HOWTO:
   https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
"""

from serialHandler import ArduinoHandler
from threadHandler import InfiniteTimer
import database
import time

#TODO: importar comunicação com banco de dados

class data_logger_app:
    """Main Application
    This class represents the main data_logger application
    """
    def __init__(self):
        self.arduino_acq = ArduinoHandler()
        self.timer_acq = InfiniteTimer(interval=10.0,
                                       worker=self.do_acquisition,
                                       on_end_function=self.close_connections)
        self.database = database.Banco('database_italo','arduinoproject',
                                        'postgres','banco')

    def insert_new_measure_into_db(self, temperature, humidity):
        # self.database.insertDataInto(table='physical_quantity',
        #                         description='temperature',
        #                         unity='Xablaus')
        self.database.insertDataInto(table='measures',
                                read_value=temperature)

        # self.database.insertDataInto(table='physical_quantity',
        #                         description='humidity',
        #                         unity='Nao Sei')
        self.database.insertDataInto(table='measures',
                                read_value=humidity)

    def run(self):
        self.start()
        self.timer_acq.start()

    def start(self):
        print("Started")
        self.database.connection()
        self.arduino_acq.open()
        time.sleep(1)

    def close_connections(self):
        print("Finalizado")

    def do_acquisition(self):
        """Pega um valor do arduino e envia para o banco de dados
        Envia o comando de ler para o arduino
        Envia para o banco de dados
        """
        # TODO: Fazer do_acquisition method
        # arduino_acq.get_readings_dict
        # database.insert()
        readings = self.arduino_acq.get_readings_dict()
        print("Leituras" + str(readings))
        self.insert_new_measure_into_db(readings['Temperatura'], readings['Umidade'])
        self.database.selectAllDataFrom(table='measures')

def menu():
    print('--------------- MENU -----------------------')
    print('0 - EXIT PROGRAM')
    print('1 - Read values')
    print('2 - Start Timer')
    print('4 - Visualize the last record')
    print('5 - Visualize all record')
    print('6 - Delete last record')
    print('7 - Delete all record')
    print('------------------------------------------\n')

import time
def main():
    main_app = data_logger_app()
    main_app.run()
    #time.sleep(2)
    #main_app.do_acquisition()

if __name__ == '__main__':
    main()
