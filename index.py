import numpy
import os
import numpy as np
from PIL import Image
import sys
import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QInputDialog
from PyQt5.uic import loadUi
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

### for trainer ####
faces = []
IDS = []

class lib400(QDialog):
    def __init__(self):
        super(lib400, self).__init__()
        loadUi('library.ui', self)
        self.image = None
        self.loadimg.clicked.connect(self.loadclicked)
        self.detectButton.setCheckable(True)
        self.detectButton.toggled.connect(self.detect_webcam_face)
        self.face_Enabled = False
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.register, ok = QInputDialog.getText(None, 'REGISTER', 'Register (student or Staff)?: ')
        #onclick train button >>> train dataset
        self.trainButton.clicked.connect(self.loadclicked2)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.redy()


    def redy(self):
        if self.register == "student":
            self.id, ok = QInputDialog.getInt(None, 'id', 'Enter Id: ')
            self.regno, ok = QInputDialog.getText(None, 'Registration Number', 'Enter Students Registration number: ')
            self.insertIntoDb(self.id,self.regno)
        elif self.register == "staff":
            self.id, ok = QInputDialog.getInt(None, 'id', 'Enter Id: ')
            self.staffId, ok = QInputDialog.getText(None, 'STAFF ID', 'Enter Staff Id Number: ')
            self.staffdb(self.id,self.staffId)
        else:
            self.showMessageBox('Warning', 'Invalid Input')
    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    #update staff table new from library
    def staffdb(self,id,staffId):
        self.connection = sqlite3.connect("library.db")
        self.cusor = self.connection.cursor()
        self.cusor.execute('''UPDATE individualData SET Id=? WHERE RegNo =?''',(self.id, self.staffId))
        self.connection.commit()
        self.connection.close()


    #update students table new from library
    def insertIntoDb(self,id,regno):
        self.connection = sqlite3.connect("library.db")
        self.cusor = self.connection.cursor()
        self.cusor.execute('''UPDATE individualData SET Id=? WHERE RegNo =?''',(self.id, self.regno))
        self.connection.commit()
        self.connection.close()
    #start and stop decting for face onclick
    def detect_webcam_face(self, status):
        if status:
            self.detectButton.setText('Stop Detect')
            self.face_Enabled = True
        else:
            self.detectButton.setText('Start Detect')
            self.face_Enabled = False

    def loadclicked(self):
        self.loadImage()
    #start video camera in 5 seconds
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
            self.displayImage(self.image, 1)

    def detect_face(self, img):
        self.sampleNum = 0
        while True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 5, minSize=(90,90))

            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),2)

                #incrementing sample number by 1
                self.sampleNum = self.sampleNum+1
                for self.sampleNum in range(1,21):
                    cv2.imwrite("dataset/user." +str(self.id) +'.'+ str(self.sampleNum) + ".jpg", gray[y:y+h,x:x+w])

            return img
    ### trainer.py #########
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
        self.recognizer.save('trainSet/trainingData.yml')

    #####

    def displayImage(self, img, window=1):
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

cv2.destroyAllWindows()
app = QApplication(sys.argv)
window = lib400()
window.setWindowTitle('KIU lib')
window.show()
sys.exit(app.exec_())
