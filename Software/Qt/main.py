import os
import sys

from pyA20.gpio import gpio
from pyA20.gpio import port
from pyA20.gpio import connector

from orangepwm import *

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ts_ui = r"main.ui"
        uic.loadUi(ts_ui, self)
        
        gpio.init() #Initialize module. Always called first
        self.pwm = OrangePwm(100, port.PA20)
        self.pwm.start(0)

        gpio.setcfg(port.PA20, gpio.OUTPUT)  #Configure LED1 as output
        gpio.setcfg(port.PA10, gpio.OUTPUT)
        gpio.setcfg(port.PA9, gpio.OUTPUT)
        
        self.button_relay1.clicked.connect(self.button_relay1_func)
        self.button_relay2.clicked.connect(self.button_relay2_func)
        self.button_relay3.clicked.connect(self.button_relay3_func)
        self.button_exit.clicked.connect(self.exit)


        self.dial_pwm.valueChanged.connect(self.dial_pwm_change)
        self.show()

    def dial_pwm_change(self):
        print("Dial value = %i" % (self.dial_pwm.value()*10))
        self.lcd_pwm.display(self.dial_pwm.value()*10)
        self.pwm.changeDutyCycle(self.dial_pwm.value()*10)

        

    def button_relay1_func(self):
        print(self.button_relay1.isChecked())
        gpio.output(port.PA9, self.bool_to_01(self.button_relay1.isChecked()))

    def button_relay2_func(self):
        print(self.button_relay2.isChecked())
        gpio.output(port.PA10, self.bool_to_01(self.button_relay2.isChecked()))

        
    def button_relay3_func(self):
        print(self.button_relay3.isChecked())
        gpio.output(port.PA20, self.bool_to_01(self.button_relay3.isChecked()))

    def bool_to_01(self, bool_input):
        if bool_input == True:
            return 1
        else:
            return 0
    
    def exit(self):
        gpio.output(port.PA9, 0)
        gpio.output(port.PA10, 0)
        gpio.output(port.PA20, 0)
        self.pwm.stop()

        sys.exit()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
