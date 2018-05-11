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
#TODO: importar comunicação com banco de dados

class data_logger_app:
    """Main Application
    This class represents the main data_logger application
    """
    def __init__(self):
        arduino_acq = ArduinoHandler(port_name='/dev/ttyUSB0')
        pass

    def run(self):
        pass

    def start(self):
        arduino_acq.open()
        timer_acq = InfiniteTimer(interval=30.0,
         worker=self.do_acquisition,
         on_end_function=self.close_connections)
         timer_acq.start()

    def do_acquisition(self):
        """Pega um valor do arduino e envia para o banco de dados
        Envia o comando de ler para o arduino
        Envia para o banco de dados
        """
        # TODO: Fazer do_acquisition method
        # arduino_acq.get_readings_dict
        # database.insert()
        pass

def main():
    main_app = data_logger_app()
    main_app.run()

if __name__ == '__main__':
    main()
