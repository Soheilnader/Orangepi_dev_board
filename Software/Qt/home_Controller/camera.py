from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, uic

import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

import sys
import os


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        #cap = cv2.VideoCapture("http://192.168.1.184:81/stream")
        cap = cv2.VideoCapture("http://192.168.1.50:4747/video")
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class Camera(QDialog):
    def __init__(self):
        super(Camera, self).__init__()

        #uic.loadUi(r"C:\Users\Soheil\Desktop\TS QT\dialogabout.ui", self)
        super().__init__()
        ts_ui = "camera.ui"
        uic.loadUi(ts_ui, self)

        self.setFixedSize(1024, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        back_img = QPixmap(r"pic/background/main.jpg")
        self.label.setPixmap(back_img)

        self.button_back.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/back_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/back_on.png);}
        """)

        self.button_back.clicked.connect(self.exit)





        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        self.show()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
        print("Bye")


    def exit(self):

        # gpio.output(port.PA9, 0)
        # gpio.output(port.PA10, 0)
        # gpio.output(port.PA20, 0)
        # self.pwm.stop()
        self.thread.stop()
        event.accept()
        print("Bye")
        sys.exit()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        #p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)



#about_dialog = QApplication(sys.argv)

#UIdialog = UId()
#about_dialog.exec()
