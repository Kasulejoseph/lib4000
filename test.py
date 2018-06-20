import sys

from PyQt5.QtWidgets import QApplication, QInputDialog

app = QApplication(sys.argv)
Id, ok = QInputDialog.getInt(None, 'Id', 'Enter your Id: ')
print(type(Id))
sys.exit()