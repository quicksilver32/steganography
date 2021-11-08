import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from cv2 import cv2
import hashlib

import design
from utils import *


def show_message(message):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(QtWidgets.QMessageBox.Information)
    msgBox.setText(str(message))
    msgBox.setWindowTitle("Info")
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msgBox.exec_()


class App(QtWidgets.QMainWindow, design.Ui_Steganography):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.decButton.setDisabled(True)
        self.encButton.setDisabled(True)
        self.textEdit.setDisabled(True)
        self.downloadButton.setDisabled(True)
        self.secretKeyInput.setDisabled(True)
        self.imgButton.clicked.connect(self.browse_file)
        self.encButton.clicked.connect(self.encrypt_image)
        self.decButton.clicked.connect(self.decrypt_image)
        self.downloadButton.clicked.connect(self.save_file)
        self.imgFile1 = ""
        self.imgFile2 = []

    def browse_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file", "", "*.bmp")[0]

        if not file:
            return

        pixmap = QPixmap(file)
        self.imgLabel1.setPixmap(pixmap)
        self.imgLabel2.setPixmap(QPixmap())

        self.imgFile1 = file
        self.decButton.setDisabled(False)
        self.encButton.setDisabled(False)
        self.secretKeyInput.setDisabled(False)
        self.textEdit.setText("")
        self.textEdit.setDisabled(False)
        self.fileLabel.setText(file.split("/")[-1])

    def save_file(self):
        extension = "." + self.imgFile1.split(".")[-1]
        file_url = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", extension)[0]

        if not file_url:
            return

        cv2.imwrite(file_url + extension, self.imgFile2)

    def encrypt_image(self):
        secret_key = self.secretKeyInput.text()
        text = self.textEdit.toPlainText()

        if secret_key == "" or text == "":
            show_message("Secret Key and Text fields must be filled!")
            return

        img = cv2.imread(self.imgFile1)

        if len(text) > img.shape[0]*img.shape[1]:
            show_message("Text is too long for this picture")

        secret_key = hashlib.md5(secret_key.encode())
        print(secret_key)
        result = encrypt_image(img, text+"\0", secret_key)
        image = QtGui.QImage(result.data, result.shape[1], result.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.imgLabel2.setPixmap(QPixmap.fromImage(image))
        self.imgFile2 = result
        self.downloadButton.setDisabled(False)

    def decrypt_image(self):
        secret_key = self.secretKeyInput.text()

        if secret_key == "":
            show_message("Secret Key field must be filled!")
            return

        secret_key = hashlib.md5(secret_key.encode())
        img = cv2.imread(self.imgFile1)
        result = decrypt_image(img, secret_key)
        self.textEdit.setText(result)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
