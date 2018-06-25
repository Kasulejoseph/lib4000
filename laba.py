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
        loadUi('library.ui', self)
        self.image = None
        self.loadimg.clicked.connect(self.loadclicked)
        self.detectButton.setCheckable(True)
        self.detectButton.toggled.connect(self.detect_webcam_face)
        self.face_Enabled = False
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.id, ok = QInputDialog.getInt(None, 'id', 'Enter Id: ')
        self.regno, ok = QInputDialog.getText(None, 'Registration Number', 'Enter Students Registration number: ')
        self.name, ok = QInputDialog.getText(None, 'name', 'Enter Students Name: ')
        self.nationality, ok = QInputDialog.getText(None, 'Nationality', 'Enter Students Nationality: ')
        self.college, ok = QInputDialog.getText(None, 'College or School', 'Enter Students College Name: ')
        self.course, ok = QInputDialog.getText(None, 'Program or Course', 'Enter Students Course: ')
        self.year, ok = QInputDialog.getText(None, 'Year and Semester', 'Enter Students Year and Semester: ')

        self.connection = sqlite3.connect("library.db")

        self.insertIntoDb()

    def insertIntoDb(self):
        self.cusor = self.connection.cursor()
        self.cusor.execute('''CREATE TABLE IF NOT EXISTS students(Id INTEGER , RegNo TEXT , Name TEXT,
                            Nationality TEXT, College TEXT, Course TEXT, Year TEXT)''')
        self.cusor.execute('SELECT * FROM students WHERE Id = "str(self.id)"')
        isRecordExist = 0
        for row in self.cusor:
            isrecordExist = 1
        if (isRecordExist == 1):
            self.cusor.execute('''UPDATE student SET RegNo ="+self.regno+", Name="+self.name+",
             Nationality="+self.nationality+", College="+self.college+", Course="+self.course+", Year="+self.year+"
              WHERE Id=?, (str(self.id)) ''')
        else:
            self.cusor.execute('''INSERT INTO students(Id, RegNo, Name, Nationality, College, Course, Year)
            VALUES(?,?,?,?,?,?,?)''', (self.id, self.regno, self.name, self.nationality, self.college, self.course, self.year))
        self.connection.commit()
        self.connection.close()


    def detect_webcam_face(self, status):
        if status:
            self.detectButton.setText('Stop Detect')
            self.face_Enabled = True
        else:
            self.detectButton.setText('Start Detect')
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
                for self.sampleNum in range(1,10):
                    cv2.imwrite("dataset/user." +str(self.id) +'.'+ str(self.sampleNum) + ".jpg", gray[y:y+h,x:x+w])

            return img

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

app = QApplication(sys.argv)
window = lib400()
window.setWindowTitle('kIU lib')
window.show()
sys.exit(app.exec_())
