import numpy
import sys
import cv2
import time
import datetime
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
        #self.id =0
        self.profile= None

        self.connection = sqlite3.connect("library.db")
        self.conn = sqlite3.connect("finance.db")


    def getdata(self, id):
        self.connection2 = sqlite3.connect("library.db")
        cmd = "SELECT * FROM individualData WHERE Id ="+str(id)
        cursor = self.connection2.execute(cmd)
        for row in cursor:
            self.profile = row
        self.connection2.close()

        return self.profile
        self.detect_face(self.profile)

    #create a report table
    def report(self):
        id=0
        self.cusor = self.connection.cursor()
        self.cusor.execute('''CREATE TABLE IF NOT EXISTS report(Id INTEGER , Name TEXT, RegNo TEXT UNIQUE,
                            Date TEXT)''')
        self.profile = self.getdata(id)
        id = self.profile[0]
        name = self.profile[2]
        regno = self.profile[1]
        date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        self.cusor.execute("SELECT * FROM report WHERE Id="+str(id))
        isRecordExist = 0
        for row in self.cusor:
            isRecordExist = 1
        if (isRecordExist == 1):
            self.cusor.execute('''UPDATE OR IGNORE report SET RegNo ="+regno+", Name="+name+",Date="+date+"
              WHERE Id="+str(id)+" ''')
        else:
            self.cusor.execute('''INSERT OR IGNORE INTO report(Id, Name, RegNo, Date)
            VALUES(?,?,?,?)''', (id, name, regno, date))
        self.connection.commit()



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
            detected_image = self.detect_face(self.image, self.profile)
            self.displayImage(detected_image,1)
        else:
            self.displayImage(self.image, 2)

    def detect_face(self, img,data):
        self.rec.read('trainSet/trainingData.yml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(90,90))
        Id = None
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),2)
            Id, conf = self.rec.predict(gray[y:y+y,x:x+w])
            self.profile = self.getdata(Id)
            if self.profile != None:

                if Id == 22:
                    cv2.putText(img, str(self.profile[2]), (x, y + h + 60), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[1]), (x, y + h + 30), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[5]), (x, y + h + 90), self.font, 1, (0, 0, 255), 2)
                    self.report()
                elif Id == 70:
                    cv2.putText(img, str(self.profile[2]), (x, y + h + 20), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[1]), (x, y + h + 120), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[5]), (x, y + h + 90), self.font, 1, (0, 0, 255), 2)
                    self.report()
                elif Id == 765:
                    cv2.putText(img, str(self.profile[2]), (x, y + h + 60), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[1]), (x, y + h + 20), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[5]), (x, y + h + 120), self.font, 1, (0, 0, 255), 2)
                    self.report()
                elif Id == 200:
                    cv2.putText(img, str(self.profile[2]), (x, y + h + 60), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[1]), (x, y + h + 30), self.font, 1, (0, 0, 255), 2)
                    cv2.putText(img, str(self.profile[5]), (x, y + h + 90), self.font, 1, (0, 0, 255), 2)
                    self.report()     
                else:
                    cv2.putText(img, "UKNOWN PERSON", (x, y + h + 30), self.font, 2, (0, 0, 255), 2)

           # else:
                #continue
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
