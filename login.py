# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
import sqlite3

from PyQt6 import QtCore, QtGui, QtWidgets
#import Ui_Signup
from PyQt6.QtWidgets import QMessageBox

class Ui_Dialog(object):
    def showMessageBox(self,title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
        msgBox.exec()
    def signupShow(self):
        self.signUpWindow = QtWidgets.QDialog()
        self.ui = Ui_Signup()
        self.ui.setupUi(self.signUpWindow)
        self.signUpWindow.show()
    def loginCheck(self):
        username = self.uname_lineEdit.text()
        password = self.pass_lineEdit.text()

        self.con = sqlite3.connect("login.db")
        self.cusor = self.con.cursor()
        result = self.cusor.execute("SELECT * FROM USERS WHERE USERNAME =? AND PASSWORD =?",(username,password))

        if (len(result.fetchall())>0):
            print("user verified")
        else:
            print("user not found")
            self.showMessageBox('Warning','Invalid username or password')
        self.con.commit()
        self.con.close()
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(583, 490)
        self.uname_label = QtWidgets.QLabel(Dialog)
        self.uname_label.setGeometry(QtCore.QRect(120, 180, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.uname_label.setFont(font)
        self.uname_label.setObjectName("uname_label")
        self.pass_label = QtWidgets.QLabel(Dialog)
        self.pass_label.setGeometry(QtCore.QRect(120, 250, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pass_label.setFont(font)
        self.pass_label.setObjectName("pass_label")
        self.uname_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QtCore.QRect(230, 180, 171, 31))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.pass_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QtCore.QRect(230, 246, 171, 31))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.login_btn = QtWidgets.QPushButton(Dialog)
        self.login_btn.setGeometry(QtCore.QRect(200, 320, 81, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_btn.setFont(font)
        self.login_btn.setObjectName("login_btn")
        self.signup_btn = QtWidgets.QPushButton(Dialog)
        self.signup_btn.setGeometry(QtCore.QRect(320, 320, 81, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.signup_btn.setFont(font)
        self.signup_btn.setObjectName("signup_btn")
        ################################## button event #################
        self.login_btn.clicked.connect(self.loginCheck)
        ################################################################################
        self.signup_btn.clicked.connect(self.signupShow)
        ################################################################################
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 50, 291, 101))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        ####################
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.uname_label.setText(_translate("Dialog", "USERNAME"))
        self.pass_label.setText(_translate("Dialog", "PASSWORD"))
        self.login_btn.setText(_translate("Dialog", "Login"))
        self.signup_btn.setText(_translate("Dialog", "Sign Up"))
        self.label.setText(_translate("Dialog", "ADMINISTRATOR LOGIN"))



###########################################
class Ui_Signup(object):
    def signupDatabase(self):
        username = self.uname_lineEdit.text()
        email = self.email_lineEdit.text()
        password = self.pass_lineEdit.text()

        self.con = sqlite3.connect("login.db")

        self.cusor = self.con.cursor()
        self.cusor.execute("CREATE TABLE IF NOT EXISTS USERS(USERNAME TEXT NOT NULL, EMAIL TEXT, PASSWORD TEXT)")
        self.cusor.execute("INSERT INTO USERS VALUES(?, ?, ?)",(username,email,password) )

        self.con.commit()
        self.con.close()
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(617, 562)
        self.uname_label = QtWidgets.QLabel(Dialog)
        self.uname_label.setGeometry(QtCore.QRect(130, 190, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.uname_label.setFont(font)
        self.uname_label.setObjectName("uname_label")
        self.email_label = QtWidgets.QLabel(Dialog)
        self.email_label.setGeometry(QtCore.QRect(130, 250, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")
        self.pass_label = QtWidgets.QLabel(Dialog)
        self.pass_label.setGeometry(QtCore.QRect(130, 320, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pass_label.setFont(font)
        self.pass_label.setObjectName("pass_label")
        self.uname_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QtCore.QRect(260, 190, 231, 31))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.email_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QtCore.QRect(260, 260, 231, 31))
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.pass_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QtCore.QRect(260, 320, 231, 31))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.signup_btn = QtWidgets.QPushButton(Dialog)
        self.signup_btn.setGeometry(QtCore.QRect(260, 390, 81, 27))
        self.signup_btn.setObjectName("signup_btn")
        self.login_btn = QtWidgets.QPushButton(Dialog)
        self.login_btn.setGeometry(QtCore.QRect(390, 390, 71, 27))
        self.login_btn.setObjectName("login_btn")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 40, 421, 111))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")

        ############################database ###############
        self.signup_btn.clicked.connect(self.signupDatabase)
        #######################################################
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.uname_label.setText(_translate("Dialog", "USERNAME"))
        self.email_label.setText(_translate("Dialog", "EMAIL"))
        self.pass_label.setText(_translate("Dialog", "PASSWORD"))
        self.signup_btn.setText(_translate("Dialog", "Sign Up"))
        self.login_btn.setText(_translate("Dialog", "Login"))
        self.label_4.setText(_translate("Dialog", "CREATE ADMIN ACCOUNT"))


###################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())

    ######################################################################################


