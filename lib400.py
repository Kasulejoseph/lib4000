import sys
import os
import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class lib400(QDialog):
    def __init__(self):
        super(lib400, self).__init__()
        loadUi('library.ui', self)
        self.image = None
        self.loadimg.clicked.connect(self.loadclicked)
        self.path = 'dataset'
        self.imagepaths = [os.path.join(self.path, f) for f in os.listdir(self.path)]

    @pyqtSlot()
    def loadclicked(self):
        tu = 0

        for self.imagepath in self.imagepaths:
            tu = tu + 1
            for tu in range(1,len(self.imagepaths)):
                self.loadImage(self.imagepath)

    def loadImage(self, fname):
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        self.displayImage()

    def displayImage(self):
        qformat = QImage.Format_Indexed8

        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        #BRG>RGB
        img = img.rgbSwapped()
        self.imglabel.setPixmap(QPixmap.fromImage(img))
        self.imglabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)


app = QApplication(sys.argv)
window = lib400()
window.setWindowTitle('kIU lib')
window.show()
sys.exit(app.exec_())
