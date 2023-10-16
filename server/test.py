from flask import Flask, Response
from flask_cors import CORS
from PyQt6.QtCore import pyqtSlot, QTimer, pyqtSignal, QThread, QObject
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit, QInputDialog
import numpy
import sys
import cv2
import time
import datetime
import threading
import queue

app = Flask(__name__)
CORS(app)

def gen(camera):
    while True:
        frame = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        
class MyThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        
    def run(self):
        self.camera.intReady.connect(self.onIntReady)
        self.camera.finished.connect(self.quit)
        self.camera.loadImage()

    @pyqtSlot(int)
    def onIntReady(self, i):
        print(i)
        
        
class FrameBuffer(threading.Thread):
    def __init__(self):
        super(FrameBuffer, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.buffer = queue.Queue(maxsize=10)
        self.stopped = False

    def run(self):
        while not self.stopped:
            if not self.buffer.full():
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.buffer.put(frame)

    def get_frame(self):
        return self.buffer.get()

    def stop(self):
        self.stopped = True
  

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
        
        self.buffer = FrameBuffer()
        self.buffer.start()
        
        
        # self.loadclicked()
        # self.detect_webcam_face(self.status)
        
        
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
        self.image = self.buffer.get_frame()
        self.image = cv2.flip(self.image, 1)

        if (self.face_enabled):
            detected_image = self.detect_face(self.image, self.profile)
            self.displayImage(detected_image,1)
        else:
            self.displayImage(self.image, 2)
            
    def displayImage(self, img, window=2):
        self.image = img
        
    def get_frame(self):
        return self.image
        
        
@app.route("/start_camera", methods=['GET'])
def initiate_camera():
    camera = Recognizer()
    thread = MyThread(camera)
    thread.start()
    thread.wait()
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
        

