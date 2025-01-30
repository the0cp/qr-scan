# This Python file uses the following encoding: utf-8
from sys import exit, argv
from re import compile, match, IGNORECASE
from webbrowser import open as web_open
from keyboard import add_hotkey
from collections import deque
from cv2 import cvtColor, COLOR_RGBA2BGR
from numpy import array
from zxingcpp import read_barcodes
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSystemTrayIcon,
    QMenu, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QMessageBox
)
from PySide6.QtGui import (
    QPixmap, QImage, QGuiApplication, QScreen,
    QPainter, QPen, QColor, QIcon, QAction
)
from PySide6.QtCore import Qt, QTimer, QMetaObject, Slot, QSettings, QSharedMemory

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
#     pyside6-uic codebarwindow.ui -o ui_codebarwindow.py
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
        shadow = QWidget(self)
        shadow.setGeometry(0, 0, self.width(), self.height())
        shadow.setStyleSheet("QWidget{border-radius:10px; background-color:rgba(32,32,32,160);}")
        shadow.lower()

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
        url_regex = compile(
            r'^[a-zA-Z][a-zA-Z\d+\-.]*://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|' # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ipv6
            r'(?::\d+)?' # port
            r'(?:/?|[/?]\S+)$', IGNORECASE)
        return match(url_regex, text) is not None

class QrHelper(QMainWindow):
    def __init__(self, parent=None):
        super(QrHelper, self).__init__(parent)
        self.ui = Ui_QrHelper()
        self.ui.setupUi(self)
        self.overlay = Overlay()
        self.codebar_windows = []
        self.recent = deque(maxlen=20)

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
        self.tray_icon.activated.connect(lambda reason: self.show() if reason == QSystemTrayIcon.DoubleClick else None)
        self.tray_icon.show()

        self.scroll_layout = QVBoxLayout(self.ui.scroll_widget)

        self.ui.clear_button.clicked.connect(self.clear_all)

        self.setWindowIcon(QIcon(":/icons/icon.png"))

        self.ui.show_pop.toggled.connect(self.save_settings)
        self.ui.show_list.toggled.connect(self.save_settings)

        settings = QSettings("the0cp", "qr-scan")
        selected_option = settings.value("selected_option", "Popup")
        if selected_option == "Popup":
            self.ui.show_pop.setChecked(True)
        else:
            self.ui.show_list.setChecked(True)

        add_hotkey('ctrl+shift+q', lambda: QMetaObject.invokeMethod(self, "capture_and_decode", Qt.QueuedConnection))

        self.shared_memory = QSharedMemory("SingleInstanceAppKey")
        if not self.shared_memory.create(1):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText("Another instance of QR Scanner is already running.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setWindowIcon(QIcon(":/icons/icon.png"))
            msg_box.exec()
            exit(1)

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
        barcodes = read_barcodes(image)
        if len(barcodes) == 0:
            print("Could not find any barcode.")
            return -1

        settings = QSettings("the0cp", "qr-scan")
        selected_option = settings.value("selected_option", "Popup")
        for barcode in barcodes:
            self.recent.append(barcode.text)

        if selected_option == "Popup":
            if self.codebar_windows:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Warning")
                msg_box.setText("Close all popups first")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.setWindowIcon(QIcon(":/icons/icon.png"))
                msg_box.exec()
                return 0
            else:
                for barcode in barcodes:
                    self.show_code_bar_window(barcode)
                self.update_recent()
                return 0
        self.update_recent()
        self.show();
        return 0

    def update_recent(self):
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.scroll_layout.removeItem(item)
        for text in self.recent:
            self.add_recent_unit(text)

    def add_recent_unit(self, text):
        text_edit = QTextEdit()
        text_edit.setText(text)
        text_edit.setFixedSize(265, 35)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("QTextEdit { border: 2px solid palette(dark); border-radius: 10px}")

        copy_button = QPushButton()
        open_button = QPushButton()
        delete_button = QPushButton()
        copy_button.setIcon(QIcon(":/icons/copy.png"))
        open_button.setIcon(QIcon(":/icons/open.png"))
        delete_button.setIcon(QIcon(":/icons/close.png"))
        copy_button.setFixedSize(35, 35)
        open_button.setFixedSize(35, 35)
        delete_button.setFixedSize(35, 35)

        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(text))
        open_button.clicked.connect(lambda: webbrowser.open(text))
        delete_button.clicked.connect(lambda: self.remove_recent_unit(unit_frame, text))

        unit_layout = QHBoxLayout()
        unit_layout.setSpacing(0)
        unit_layout.addWidget(text_edit)
        unit_layout.addWidget(copy_button)
        unit_layout.addWidget(open_button)
        unit_layout.addWidget(delete_button)

        unit_frame = QFrame()
        unit_frame.setLayout(unit_layout)
        unit_frame.setFixedSize(410, 55)
        unit_frame.setStyleSheet("""
            QFrame#UnitFrame{
                border: 1px solid #235f73;
                border-radius: 10px;
            }
            """)
        unit_frame.setObjectName("UnitFrame")
        self.scroll_layout.insertWidget(0, unit_frame)
        self.scroll_layout.addStretch()

    def remove_recent_unit(self, unit_frame, text):
        self.scroll_layout.removeWidget(unit_frame)
        unit_frame.setParent(None)
        if text in self.recent:
            self.recent.remove(text)

    def show_code_bar_window(self, barcode):
        position = barcode.position
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = position.bottom_left.x
        y = position.bottom_left.y
        width = 300
        height = 70

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

    def clear_all(self):
        self.recent.clear()
        for window in self.codebar_windows:
            window.close()
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.scroll_layout.removeItem(item)

    def pixmap2cv(self, pixmap):
        qimage = pixmap.toImage()
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        arr = array(ptr).reshape((height, width, 4))  # RGBA Array
        return cvtColor(arr, COLOR_RGBA2BGR)

    def save_settings(self):
        settings = QSettings("the0cp", "qr-scan")
        settings.setValue("selected_option", "Popup" if self.ui.show_pop.isChecked() else "List")

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def exit_app(self):
        for window in self.codebar_windows:
            window.close()
        self.tray_icon.hide()
        QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(argv)
    app.setQuitOnLastWindowClosed(False)
    widget = QrHelper()
    widget.hide()
    exit(app.exec())
