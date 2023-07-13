import os
import sys
from random import randint

from pyA20.gpio import gpio
from pyA20.gpio import port
from pyA20.gpio import connector
import serial

#from orangepwm import *

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ts_ui = r"main.ui"
        uic.loadUi(ts_ui, self)
        self.UART_STATUS = False
        try:
            self.ser = serial.Serial('/dev/ttyS1', baudrate = 9600, timeout = 0.5)
            self.UART_STATUS = True            
        except:
            print("UART error")
            
        gpio.init() #Initialize module. Always called first
        #self.pwm = OrangePwm(100, port.PA20)
        #self.pwm.start(0)

        gpio.setcfg(port.PA20, gpio.OUTPUT)  #Configure LED1 as output
        gpio.setcfg(port.PA10, gpio.OUTPUT)
        gpio.setcfg(port.PA9, gpio.OUTPUT)
        
        self.button_relay1.clicked.connect(self.button_relay1_func)
        self.button_relay2.clicked.connect(self.button_relay2_func)
        self.button_relay3.clicked.connect(self.button_relay3_func)
        self.button_exit.clicked.connect(self.exit)
        self.dial_pwm.valueChanged.connect(self.dial_pwm_change)
   
        self.progress_adc.setRange(0, 100)

        self.x = list(range(100))  # 100 time points
        self.y = [0 for _ in range(100)]  # 100 data points
        
        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
   

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        #self.y.append(randint(0, 100)*3.3/100)  # Add a new random value.
        if self.UART_STATUS:
            self.y.append(self.getValues())  # Add a new random value.            
        self.progress_adc.setValue(int(self.y[-1]*100/3.3))
        self.lcd_adc.display(self.y[-1])
        self.data_line.setData(self.x, self.y)  # Update the data.


        
        self.show()

    def getValues(self):
        self.ser.write(b'0')
        data = self.ser.readline().decode('ascii')
        return float(data)

    def dial_pwm_change(self):
        print("Dial value = %i" % (self.dial_pwm.value()*10))
        self.lcd_pwm.display(self.dial_pwm.value()*10)
        #self.pwm.changeDutyCycle(self.dial_pwm.value()*10)

        

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
        #self.pwm.stop()
        if self.UART_STATUS:
            self.ser.close()
        sys.exit()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
