import os
import sys
from random import randint

import serial


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
                  
  
        self.button_exit.clicked.connect(self.exit)


        self.x0 = list(range(100))  # 100 time points
        self.y0 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget0.setBackground('w')

        self.x1 = list(range(100))  # 100 time points
        self.y1 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget1.setBackground('w')

        self.x2 = list(range(100))  # 100 time points
        self.y2 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget2.setBackground('w')

        self.x3 = list(range(100))  # 100 time points
        self.y3 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget3.setBackground('w')

        self.x4 = list(range(100))  # 100 time points
        self.y4 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget4.setBackground('w')

        self.x5 = list(range(100))  # 100 time points
        self.y5 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget5.setBackground('w')

        self.x6 = list(range(100))  # 100 time points
        self.y6 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget6.setBackground('w')

        self.x7 = list(range(100))  # 100 time points
        self.y7 = [0 for _ in range(100)]  # 100 data points
        self.graphWidget7.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line0 = self.graphWidget0.plot(self.x0, self.y0, pen=pen)
        self.data_line1 = self.graphWidget1.plot(self.x1, self.y1, pen=pen)
        self.data_line2 = self.graphWidget2.plot(self.x2, self.y2, pen=pen)
        self.data_line3 = self.graphWidget3.plot(self.x3, self.y3, pen=pen)
        self.data_line4 = self.graphWidget4.plot(self.x4, self.y4, pen=pen)
        self.data_line5 = self.graphWidget5.plot(self.x5, self.y5, pen=pen)
        self.data_line6 = self.graphWidget6.plot(self.x6, self.y6, pen=pen)
        self.data_line7 = self.graphWidget7.plot(self.x7, self.y7, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
   

    def update_plot_data(self):
        if self.checkbox_adc0.isChecked():
            self.x0 = self.x0[1:]  # Remove the first y element.
            self.x0.append(self.x0[-1] + 1)  # Add a new value 1 higher than the last.
            self.y0 = self.y0[1:]  # Remove the first
            #self.y0.append(randint(0, 100)*3.3/100)  # Add a new random value.
            if self.UART_STATUS:
                self.y0.append(self.getValues(0))  # Add a new random value.  
            self.data_line0.setData(self.x0, self.y0)  # Update the data.
            self.lcd_adc0.display(self.y0[-1])

        if self.checkbox_adc1.isChecked():
            self.x1 = self.x1[1:]  # Remove the first y element.
            self.x1.append(self.x1[-1] + 1)  # Add a new value 1 higher than the last.
            self.y1 = self.y1[1:]  # Remove the first
            #self.y1.append(randint(0, 100)*3.3/100)  # Add a new random value.
            if self.UART_STATUS:
                self.y1.append(self.getValues(1))  # Add a new random value.  
            self.data_line1.setData(self.x1, self.y1)  # Update the data.
            self.lcd_adc1.display(self.y1[-1])

        if self.checkbox_adc2.isChecked():
            self.x2 = self.x2[1:]  # Remove the first y element.
            self.x2.append(self.x2[-1] + 1)  # Add a new value 1 higher than the last.
            self.y2 = self.y2[1:]  # Remove the first
            self.y2.append(randint(0, 100)*3.3/100)  # Add a new random value.
            self.data_line2.setData(self.x2, self.y2)  # Update the data.
            self.lcd_adc2.display(self.y2[-1])

        if self.checkbox_adc3.isChecked():
            self.x3 = self.x3[1:]  # Remove the first y element.
            self.x3.append(self.x3[-1] + 1)  # Add a new value 1 higher than the last.
            self.y3 = self.y3[1:]  # Remove the first
            self.y3.append(randint(0, 100)*3.3/100)  # Add a new random value.
            self.data_line3.setData(self.x3, self.y3)  # Update the data.
            self.lcd_adc3.display(self.y3[-1])

        if self.checkbox_adc4.isChecked():
            self.x4 = self.x4[1:]  # Remove the first y element.
            self.x4.append(self.x4[-1] + 1)  # Add a new value 1 higher than the last.
            self.y4 = self.y4[1:]  # Remove the first
            self.y4.append(randint(0, 100)*3.3/100)  # Add a new random value.
            self.data_line4.setData(self.x4, self.y4)  # Update the data.
            self.lcd_adc4.display(self.y4[-1])

        if self.checkbox_adc5.isChecked():
            self.x5 = self.x5[1:]  # Remove the first y element.
            self.x5.append(self.x5[-1] + 1)  # Add a new value 1 higher than the last.
            self.y5 = self.y5[1:]  # Remove the first
            self.y5.append(randint(0, 100)*3.3/100)  # Add a new random value.
            self.data_line5.setData(self.x5, self.y5)  # Update the data.
            self.lcd_adc5.display(self.y5[-1])

        if self.checkbox_adc6.isChecked():
            self.x6 = self.x6[1:]  # Remove the first y element.
            self.x6.append(self.x6[-1] + 1)  # Add a new value 1 higher than the last.
            self.y6 = self.y6[1:]  # Remove the first
            self.y6.append(randint(0, 100)*3.3/100)  # Add a new random value.
            self.data_line6.setData(self.x6, self.y6)  # Update the data.
            self.lcd_adc6.display(self.y6[-1])

        if self.checkbox_adc7.isChecked():
            self.x7 = self.x7[1:]  # Remove the first y element.
            self.x7.append(self.x7[-1] + 1)  # Add a new value 1 higher than the last.
            self.y7 = self.y7[1:]  # Remove the first
            self.y7.append(randint(0, 100)*3.3/100)  # Add a new random value.
            self.data_line7.setData(self.x7, self.y7)  # Update the data.
            self.lcd_adc7.display(self.y7[-1])

        
        self.show()

    def getValues(self, pin):
        if pin==0:    
            self.ser.write(b'0')
        elif pin==1:    
            self.ser.write(b'1')
        data = self.ser.readline().decode('ascii')
        return float(data)
    
    def exit(self):
        if self.UART_STATUS:
            self.ser.close()
        sys.exit()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
