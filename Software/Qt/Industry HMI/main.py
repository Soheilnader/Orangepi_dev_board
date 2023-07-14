import os
import sys
import time
from random import randint

from pyA20.gpio import gpio
from pyA20.gpio import port
from pyA20.gpio import connector

import serial

from orangepwm import *

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer



class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ts_ui = r"main.ui"
        uic.loadUi(ts_ui, self)
        self.setFixedSize(1024, 600)

        self.rpm1 = 0
        self.rpm3 = 0
        self.rpm4 = 0


        self.UART_STATUS = False
        
        try:
            self.ser = serial.Serial('/dev/ttyS1', baudrate=9600, timeout=0.5)
            self.UART_STATUS = True
        except:
            print("UART error")

        gpio.init()  # Initialize module. Always called first
        self.pwm = OrangePwm(100, port.PA7)
        self.pwm.start(0)

        gpio.setcfg(port.PA10, gpio.OUTPUT)  # Configure LED1 as output
        gpio.setcfg(port.PA9, gpio.OUTPUT)
        gpio.setcfg(port.PA21, gpio.OUTPUT)


        self.button_pump1.clicked.connect(self.button_pump1_clicked)
        self.button_pump4.clicked.connect(self.button_pump4_clicked)
        self.button_pump3.clicked.connect(self.button_pump3_clicked)
        self.button_exit.clicked.connect(self.exit)
        self.dial_pump.valueChanged.connect(self.dial_pump_change)



        self.x = list(range(100))  # 100 time points
        self.y1 = [0 for _ in range(100)]  # 100 data points
        self.y2 = [0 for _ in range(100)]  # 100 data points
        
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


        back_img = QPixmap(r"back_img.jpg")
        self.img_back.setPixmap(back_img)

        usc_img = QPixmap(r"logo.png")
        self.img_usc.setPixmap(usc_img)

        self.show()
    '''        
    def getValues(self):
        self.ser.write(b'0')
        data = self.ser.readline().decode('ascii')
        return float(data)
    '''

    def getValues(self, pin):
        if pin==0:    
            self.ser.write(b'0')
        elif pin==1:    
            self.ser.write(b'1')
        data = self.ser.readline().decode('ascii')
        return float(data)

    def button_pump1_clicked(self):
        print(self.button_pump1.isChecked())
        gpio.output(port.PA9, self.bool_to_01(self.button_pump1.isChecked()))
        if self.button_pump1.isChecked():
            self.rpm1 = 1000
        if not self.button_pump1.isChecked():
            self.rpm1 = 0
        self.lcd_rpm1.display(self.rpm1)

    def button_pump4_clicked(self):
        print(self.button_pump4.isChecked())
        gpio.output(port.PA10, self.bool_to_01(self.button_pump4.isChecked()))
        if self.button_pump4.isChecked():
            self.rpm4 = 1000
        if not self.button_pump4.isChecked():
            self.rpm4 = 0
        self.lcd_rpm4.display(self.rpm4)

    def button_pump3_clicked(self):
        print(self.button_pump3.isChecked())

        if (self.button_pump3.isChecked()):
            print(self.dial_pump.value())
            self.rpm3 = self.dial_pump.value() * 200
            gpio.output(port.PA21, self.bool_to_01(self.button_pump3.isChecked()))
            self.pwm.changeDutyCycle(self.dial_pump.value() * 20)
            #self.lcd_fan.display(self.dial_pump.value())
        if (not self.button_pump3.isChecked()):
            self.rpm3 = 0

            #self.lcd_fan.display(0)
            gpio.output(port.PA21, self.bool_to_01(self.button_pump3.isChecked()))
            self.pwm.changeDutyCycle(0)
            print("off")
        self.lcd_rpm3.display(self.rpm3)

    def dial_pump_change(self):
        print(self.dial_pump.value())
        if (self.button_pump3.isChecked()):
            print(self.dial_pump.value())
            self.rpm3 = self.dial_pump.value() * 200
            #self.lcd_fan.display(self.dial_pump.value())
            self.pwm.changeDutyCycle(self.dial_pump.value() * 20)
        else:
            self.rpm3 = 0
            #self.lcd_fan.display(0)
            gpio.output(port.PA21, self.bool_to_01(self.button_pump3.isChecked()))
            self.pwm.changeDutyCycle(0)
            print("off")
        self.lcd_rpm3.display(self.rpm3)


    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y1 = self.y1[1:]  # Remove the first
        self.y2 = self.y2[1:]  # Remove the first
        
        if self.UART_STATUS:
            self.y1.append(self.getValues(0))  # Add a new random value.
            self.y2.append(self.getValues(1))  # Add a new random value.
        else:
            self.y1.append(randint(0, 100) * 3.3 * 15 / 100)  # Add a new random value.
            self.y2.append(randint(0, 100) * 3.3 * 15 / 100)  # Add a new random value.
        self.progress_tank1.setValue(int(self.y1[-1] * 100 / (3.3)))
        self.progress_tank2.setValue(int(self.y2[-1] * 100 / (3.3)))
        self.progress_tank3.setValue(int((int(self.y1[-1] * 100 / (3.3)) + int(self.y2[-1] * 100 / (3.3)))/2))
        #self._lcdadc.display(self.y1[-1])
        self.temp1 = randint(30, 35)
        self.temp2 = randint(30, 35)
        self.temp3 = float((self.temp1 + self.temp2) / 2)
        self.gpm1 = float(self.rpm1 / 20)
        self.gpm2 = (self.rpm3 + self.rpm4) / 30
        self.hum = (randint(40, 50) / 1)

        self.lcd_temp1.display(self.temp1)
        self.lcd_temp2.display(self.temp2)
        self.lcd_temp3.display(self.temp3)
        self.lcd_gpm1.display(self.gpm1)
        self.lcd_gpm2.display(self.gpm2)
        self.lcd_hum.display(self.hum)

    def bool_to_01(self, bool_input):
        if bool_input == True:
            return 1
        else:
            return 0


    def exit(self):
        gpio.output(port.PA9, 0)
        gpio.output(port.PA10, 0)
        gpio.output(port.PA21, 0)
        self.pwm.stop()
        if self.UART_STATUS:
            self.ser.close()

        sys.exit()

app = QApplication(sys.argv)
UIWindow = UI()
app.exec()