from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap

import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import requests

import sys
import os



class Weather(QDialog):
    def __init__(self):
        super(Weather, self).__init__()

        #uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogabout.ui", self)
        super().__init__()
        ts_ui = "weather.ui"
        uic.loadUi(ts_ui, self)

        self.setFixedSize(1024, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        back_img = QPixmap(r"pic\background\main.jpg")
        self.label.setPixmap(back_img)

        self.button_back.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/back_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/back_on.png);}
        """)

        self.button_back.clicked.connect(self.exit)
        self.text.setText(self.Gen_report())







        self.show()

        # Function to Generate Report
    def Gen_report(self):
        url = 'https://wttr.in/{}'.format("Tehran")
        try:
            data = requests.get(url)
            T = data.text
        except:
            T = "Error Occurred"
        print(T)
        return T


    def exit(self):

        # gpio.output(port.PA9, 0)
        # gpio.output(port.PA10, 0)
        # gpio.output(port.PA20, 0)
        # self.pwm.stop()

        sys.exit()

#about_dialog = QApplication(sys.argv)

#UIdialog = UId()
#about_dialog.exec()