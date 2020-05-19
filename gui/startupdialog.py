# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startupdialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from src.analyzetr import *

class Ui_Input_File(object):
    def setupUi(self, Input_File):
        Input_File.setObjectName("Input_File")
        Input_File.setEnabled(True)
        Input_File.resize(496, 102)
        Input_File.setWindowTitle("")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Input_File.sizePolicy().hasHeightForWidth())
        Input_File.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Input_File)
        self.gridLayout.setObjectName("gridLayout")
        self.label_file = QtWidgets.QLabel(Input_File)
        self.label_file.setObjectName("label_file")
        self.gridLayout.addWidget(self.label_file, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Input_File)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.fileButton = QtWidgets.QPushButton(Input_File)
        self.fileButton.setObjectName("fileButton")
        self.gridLayout.addWidget(self.fileButton, 0, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Input_File)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 2)

        self.retranslateUi(Input_File)
        self.buttonBox.accepted.connect(Input_File.accept)
        self.buttonBox.rejected.connect(Input_File.reject)
        self.fileButton.clicked.connect(self.FilePath)
        QtCore.QMetaObject.connectSlotsByName(Input_File)

    def retranslateUi(self, Input_File):
        _translate = QtCore.QCoreApplication.translate
        Input_File.setWindowTitle(_translate("Input_File", "Input File"))
        self.label_file.setText(_translate("Input_File", "File:"))
        self.fileButton.setText(_translate("Input_File", "Open"))

    def FilePath(self):
        options = QFileDialog.Options()
        fn = QFileDialog.getOpenFileName(None,"Open File", "/home/", ("Tracer (*.tr)"))
        self.lineEdit.setText(fn[0])
        self.filename = self.lineEdit.text()
        analyzer(self.filename)
