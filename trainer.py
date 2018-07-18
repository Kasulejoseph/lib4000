import cv2
import os
import numpy as np
from PIL import Image
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

faces = []
IDS = []


class lib400(QDialog):
    def __init__(self):
        super(lib400, self).__init__()
        loadUi('library.ui', self)
        self.image = None
        self.trainButton.clicked.connect(self.loadclicked2)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()



    def loadclicked2(self):
        self.loadImage2( faces,  IDS)


    def loadImage2(self,faces,IDS):
        self.path = 'dataset'
        self.imagepaths = [os.path.join(self.path, f) for f in os.listdir(self.path)]

        for self.imagepath in self.imagepaths:
            self.faceimg = Image.open(self.imagepath).convert('L')
            self.faceNp = np.array(self.faceimg, 'uint8')
            self.ID = int(os.path.split(self.imagepath)[-1].split(".")[1])
            faces.append(self.faceNp)
            IDS.append(self.ID)


            cv2.imshow("training", self.faceNp)
            cv2.waitKey(10)
        #return np.array(IDS), faces

        #self.loadImage()

        self.recognizer.train(faces, np.array(IDS))
        self.recognizer.save('recognizer/tranningData.yml')

cv2.destroyAllWindows()

app = QApplication(sys.argv)
window = lib400()
window.setWindowTitle('kIU lib')
window.show()
sys.exit(app.exec_())
