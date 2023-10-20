from PyQt6.QtCore import pyqtSlot, pyqtSignal, QThread, QObject
import cv2
from models.library import Library
from video_processing.frame_buffer import FrameBuffer


class Recognizer(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    def __init__(self):
        super(Recognizer, self).__init__()
        self.image = None
        self.rec = cv2.face.LBPHFaceRecognizer_create()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.face_enabled = False
        self.faceCascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
        self.profile = None
        self.status = False
        self.face_enabled = True

        self.buffer = FrameBuffer()
        self.buffer.start()
        self.lib = Library()

    @pyqtSlot()
    def loadImage(self):
        i = 0
        while True:
            self.intReady.emit(i)
            self.update_frame()
            i += 1

    def update_frame(self):
        # capture frame by frame
        self.image = self.buffer.get_frame()
        # self.image = cv2.flip(self.image, 1)

        if self.face_enabled:
            detected_image = self.recognize_faces(self.image)
            self.displayImage(detected_image, 1)
        else:
            self.displayImage(self.image, 2)

    def displayImage(self, img, window=2):
        self.image = img

    def get_frame(self):
        return self.image

    def detect_faces(self, image):
        # Convert the image to grayscale for face detection
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            print(f"Error during color conversion: {e}")
            return []

        # Detect faces in the image
        try:
            faces = self.faceCascade.detectMultiScale(
                gray, 1.2, 5, minSize=(90, 90))
            return faces, gray
        except Exception as e:
            print(f"Error during face detection: {e}")
            return []

    def recognize_faces(self, img):
        self.rec.read("trainSet/trainingData3.yml")
        faces, gray = self.detect_faces(img)
        faces = self.faceCascade.detectMultiScale(
            gray, 1.2, 5, minSize=(90, 90))

        # Recognize faces in the image
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            Id, conf = self.rec.predict(gray[y: y + y, x: x + w])
            self.profile = self.lib.student_profile(Id)
            if self.profile != None:
                pass
        return img

    def stop(self):
        self.buffer.stop()
