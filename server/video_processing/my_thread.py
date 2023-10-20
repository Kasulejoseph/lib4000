from PyQt6.QtCore import QThread, pyqtSlot


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
