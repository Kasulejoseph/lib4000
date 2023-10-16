from flask import Flask, Response
from flask_cors import CORS
from PyQt6.QtCore import pyqtSlot, QTimer, pyqtSignal, QThread, QObject
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit, QInputDialog
import numpy
import sys
import cv2
import time
import datetime

app = Flask(__name__)
CORS(app)

class Recognizer(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)
    def __init__(self):
        super(Recognizer, self).__init__()
        self.image = None
        self.rec = cv2.face.LBPHFaceRecognizer_create()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.face_enabled = False
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        #self.id =0
        self.profile= None
        self.status=False
        
        # self.loadclicked()
        self.detect_webcam_face(self.status)

        
    def loadclicked(self):
        self.loadImage()
        
    def detect_webcam_face(self, status=True):
        if status:
            # self.detectButton.setText('Stop Recognition')
            self.face_enabled = True
        else:
            # self.detectButton.setText('Start Recognition')
            self.face_enabled = False
    @pyqtSlot()
    def loadImage(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        
        for i in range(1, 10):
            # time.sleep(1)
            self.intReady.emit(i)
            print("jajjajajaj")
            self.update_frame()

        self.finished.emit()
        
    def update_frame(self):
        # ca pture frame by frame
        ret, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)

        if (self.face_enabled):
            detected_image = self.detect_face(self.image, self.profile)
            self.displayImage(detected_image,1)
        else:
            self.displayImage(self.image, 2)
            

            
    def displayImage(self, img, window=2):
        # print("yeaaaaa", Response(gen(img), mimetype='multipart/x-mixed-replace; boundary=frame'))
        print(gen(img))
            
    def detect_face(self, img, data):
        self.rec.read('trainSet/trainingData.yml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(90,90))
        Id = None
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),2)
            Id, conf = self.rec.predict(gray[y:y+y,x:x+w])
            self.profile = None
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
        return img
    
    @pyqtSlot(int)
    def onIntReady(self, i):
        
        print(i)
        
    def hie(self):
        return self.image
        
        
class MyThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        
    def run(self):
        # self.camera.start()
        # worker = Recognizer()
        # print(worker.image)
        self.camera.intReady.connect(self.onIntReady)
        self.camera.finished.connect(self.quit)
        self.camera.loadImage()
        # self.exec()

    @pyqtSlot(int)
    def onIntReady(self, i):
        print(i)
        
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
  

@app.route("/start_camera", methods=['GET'])
def initiate_camera():
    # app = QApplication([])
    camera = Recognizer()
    thread = MyThread(camera)
    thread.start()
    thread.wait()
    return "hhhhhhero"

@app.route('/video_feed')
def video_feed():
    camera = Recognizer()
    thread = MyThread(camera)
    thread.start()
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=5000, debug=True)