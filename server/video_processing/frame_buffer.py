import cv2
import queue
import threading


class FrameBuffer(threading.Thread):
    def __init__(self):
        super(FrameBuffer, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.buffer = queue.Queue(maxsize=1)
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
        self.cap.release()
