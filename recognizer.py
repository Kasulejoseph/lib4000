import numpy
import sys
import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QInputDialog
from PyQt5.uic import loadUi
import sqlite3

class lib400(QDialog):
    def __init__(self):
        super(lib400, self).__init__()
        loadUi('recognize.ui', self)
        self.image = None
        self.loadimg.clicked.connect(self.loadclicked)
        self.detectButton.setCheckable(True)
        self.detectButton.toggled.connect(self.detect_webcam_face)
        self.rec = cv2.face.LBPHFaceRecognizer_create()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.face_Enabled = False
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.id =0

        self.connection = sqlite3.connect("library.db")

        self.getdata()

    def getdata(self):
        cmd = "SELECT * FROM students"
        cursor = self.connection.execute(cmd)
        print(cursor.fetchone())
        data = None
        for row in cursor:
            data = row
        return data
        self.detect_face(data)


    def detect_webcam_face(self, status):
        if status:
            self.detectButton.setText('Stop Recognition')
            self.face_Enabled = True
        else:
            self.detectButton.setText('Start Recognition')
            self.face_Enabled = False

    def loadclicked(self):
        self.loadImage()

    def loadImage(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        # capture frame by frame
        ret, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)

        if (self.face_Enabled):
            detected_image = self.detect_face(self.image)
            self.displayImage(detected_image,1)
        else:
            self.displayImage(self.image, 2)

    def detect_face(self, img):
        self.rec.read('recognizer/tranningData.yml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(90,90))

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),2)
            self.id, conf = self.rec.predict(gray[y:y + h, x:x + w])
            data = self.getdata()
            if data != None:
                if Id in data4 == 87:
                    cv2.putText(img, str(data[2]), (x, y + h + 30), self.font, 2, (0, 0, 255), 2)
                    cv2.putText(img, str(data[1]), (x, y + h + 30), self.font, 2, (0, 0, 255), 2)
                    cv2.putText(img, str(data[3]), (x, y + h + 30), self.font, 2, (0, 0, 255), 2)
                elif Id == 45:
                    self.id = "matama"
                    cv2.putText(img, str(data[1]), (x, y + h + 30), self.font, 2, (0, 0, 255), 2)
                # else:
                #     self.id = "unknown face"
                #     cv2.putText(img, str(self.id), (x, y + h + 30), self.font, 2, (0, 0, 255), 2)
            else:
                continue
        return img
        self.connection.close()

    def displayImage(self, img, window=2):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        #BRG>RGB
        outImage = outImage.rgbSwapped()
        if window==1:
            self.imglabel.setPixmap(QPixmap.fromImage(outImage))
            self.imglabel.setScaledContents(True)

app = QApplication(sys.argv)
window = lib400()
window.setWindowTitle('Recognition')
window.show()
sys.exit(app.exec_())