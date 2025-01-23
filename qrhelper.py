# This Python file uses the following encoding: utf-8
import sys
import cv2
import re
import zxingcpp
import webbrowser
import numpy as np
import keyboard
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSystemTrayIcon, QMenu, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QImage, QGuiApplication, QScreen, QPainter, QPen, QColor, QIcon, QAction
from PySide6.QtCore import Qt, QTimer, QMetaObject, Slot

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_form import Ui_QrHelper
from ui_codebarwindow import Ui_CodeBarWindow
import res_rc

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

class CodeBarWindow(QWidget):
    def __init__(self, text, format, content, position, close_callback, parent=None):
        super(CodeBarWindow, self).__init__(parent)
        self.ui = Ui_CodeBarWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(1)

        self.close_callback = close_callback

        if self.is_url(text):
            self.ui.text_box.setText(f"<a href='{text}' style='color:#7DF9FF; text-decoration:underline; font-style:italic;'>{text}</a>")
            self.ui.open_button.setEnabled(True)
        else:
            self.ui.text_box.setText(text)
            self.ui.open_button.setEnabled(False)

        self.ui.copy_button.clicked.connect(self.copy_text)
        self.ui.open_button.clicked.connect(self.open_text)
        self.ui.close_button.clicked.connect(self.close_window)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.text_box.toPlainText())
        self.close_callback(self)
        self.close()

    def open_text(self):
        webbrowser.open(self.ui.text_box.toPlainText())
        self.close_callback(self)
        self.close()

    def close_window(self):
        self.close_callback(self)
        self.close()

    def is_url(self, text):
        url_regex = re.compile(
            r'^[a-zA-Z][a-zA-Z\d+\-.]*://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|' # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ipv6
            r'(?::\d+)?' # port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(url_regex, text) is not None

class QrHelper(QMainWindow):
    def __init__(self, parent=None):
        super(QrHelper, self).__init__(parent)
        self.ui = Ui_QrHelper()
        self.ui.setupUi(self)
        self.overlay = Overlay()
        self.codebar_windows = []

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":/icons/icon.png"))
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.exit_app)
        self.tray_icon.show()

        self.setWindowIcon(QIcon(":/icons/icon.png"))

        keyboard.add_hotkey('ctrl+shift+q', lambda: QMetaObject.invokeMethod(self, "capture_and_decode", Qt.QueuedConnection))

    @Slot()
    def capture_and_decode(self):
        screenshot = self.capture_fullscreen()
        self.decode_qr(screenshot)

    def capture_fullscreen(self):
        QMetaObject.invokeMethod(self.overlay, "showFullScreen", Qt.QueuedConnection)

        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0)  # pixmap screenshot
        QTimer.singleShot(500, lambda: QMetaObject.invokeMethod(self.overlay, "hide", Qt.QueuedConnection))
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
            self.show_code_bar_window(barcode)
        return 0

    def show_code_bar_window(self, barcode):
        position = barcode.position
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = position.bottom_left.x
        y = position.bottom_left.y
        width = 420
        height = 62

        if x + width > screen.width():
            x = screen.width() - width
        if y + height > screen.height():
            y = screen.height() - height
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        code_window = CodeBarWindow(barcode.text, barcode.format, barcode.content_type, barcode.position, self.remove_code_bar_window)
        code_window.setGeometry(int(x), int(y), width, height)
        code_window.show()
        self.codebar_windows.append(code_window)  # Keep reference to the window

    def remove_code_bar_window(self, code_window):
        if code_window in self.codebar_windows:
            self.codebar_windows.remove(code_window)
        code_window.deleteLater()

    def pixmap2cv(self, pixmap):
        qimage = pixmap.toImage()
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        arr = np.array(ptr).reshape((height, width, 4))  # RGBA Array
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    widget = QrHelper()
    widget.hide()
    sys.exit(app.exec())
