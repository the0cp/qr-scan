# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'codebarwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QTextEdit,
    QWidget)
import res_rc

class Ui_CodeBarWindow(object):
    def setupUi(self, CodeBarWindow):
        if not CodeBarWindow.objectName():
            CodeBarWindow.setObjectName(u"CodeBarWindow")
        CodeBarWindow.resize(300, 70)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CodeBarWindow.sizePolicy().hasHeightForWidth())
        CodeBarWindow.setSizePolicy(sizePolicy)
        CodeBarWindow.setMinimumSize(QSize(300, 70))
        CodeBarWindow.setMaximumSize(QSize(300, 70))
        self.text_box = QTextEdit(CodeBarWindow)
        self.text_box.setObjectName(u"text_box")
        self.text_box.setGeometry(QRect(5, 5, 220, 60))
        self.text_box.setReadOnly(True)
        self.close_button = QPushButton(CodeBarWindow)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setGeometry(QRect(225, 40, 70, 25))
        font = QFont()
        font.setPointSize(9)
        font.setStyleStrategy(QFont.PreferDefault)
        font.setHintingPreference(QFont.PreferNoHinting)
        self.close_button.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close_button.setIcon(icon)
        self.copy_button = QPushButton(CodeBarWindow)
        self.copy_button.setObjectName(u"copy_button")
        self.copy_button.setGeometry(QRect(225, 5, 35, 35))
        icon1 = QIcon()
        icon1.addFile(u":/icons/copy.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.copy_button.setIcon(icon1)
        self.copy_button.setFlat(False)
        self.open_button = QPushButton(CodeBarWindow)
        self.open_button.setObjectName(u"open_button")
        self.open_button.setEnabled(False)
        self.open_button.setGeometry(QRect(260, 5, 35, 35))
        icon2 = QIcon()
        icon2.addFile(u":/icons/open.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_button.setIcon(icon2)
        self.open_button.setIconSize(QSize(16, 16))

        self.retranslateUi(CodeBarWindow)

        QMetaObject.connectSlotsByName(CodeBarWindow)
    # setupUi

    def retranslateUi(self, CodeBarWindow):
        CodeBarWindow.setWindowTitle(QCoreApplication.translate("CodeBarWindow", u"Form", None))
        self.close_button.setText(QCoreApplication.translate("CodeBarWindow", u"Cancel", None))
        self.copy_button.setText("")
        self.open_button.setText("")
    # retranslateUi

