# This Python file uses the following encoding: utf-8
import sys
import cv2
import zxingcpp
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPixmap, QImage, QGuiApplication, QScreen, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_QrHelper

class Overlay(QWidget):
    def __init__(self):
        super(Overlay, self).__init__()
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))
        painter.setPen(QPen(Qt.red, 10))
        painter.drawRect(self.rect())

class QrHelper(QMainWindow):
    def __init__(self, parent=None):
        super(QrHelper, self).__init__(parent)
        self.ui = Ui_QrHelper()
        self.ui.setupUi(self)
        self.overlay = Overlay()

        self.capture_and_decode()

    def capture_and_decode(self):
        screenshot = self.capture_fullscreen()
        self.decode_qr(screenshot)

    def capture_fullscreen(self):
        self.overlay.showFullScreen()

        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0)  # pixmap screenshot
        QTimer.singleShot(500, lambda: self.overlay.hide())
        return screenshot

    def decode_qr(self, screenshot):
        image = self.pixmap2cv(screenshot)
        barcodes = zxingcpp.read_barcodes(image)
        if len(barcodes) == 0:
            print("Could not find any barcode.")
            return -1
        for barcode in barcodes:
            print('Found barcode:'
                  f'\n Text:    "{barcode.text}"'
                  f'\n Format:   {barcode.format}'
                  f'\n Content:  {barcode.content_type}'
                  f'\n Position: {barcode.position}')
        return 0

    def pixmap2cv(self, pixmap):
        qimage = pixmap.toImage()
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        arr = np.array(ptr).reshape((height, width, 4))  # RGBA Array
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

    def closeEvent(self, event):
        self.overlay.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QrHelper()
    widget.show()
    sys.exit(app.exec())
