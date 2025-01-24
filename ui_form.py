# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QWidget)

class Ui_QrHelper(object):
    def setupUi(self, QrHelper):
        if not QrHelper.objectName():
            QrHelper.setObjectName(u"QrHelper")
        QrHelper.resize(440, 330)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QrHelper.sizePolicy().hasHeightForWidth())
        QrHelper.setSizePolicy(sizePolicy)
        QrHelper.setMinimumSize(QSize(440, 330))
        QrHelper.setMaximumSize(QSize(440, 330))
        self.scroll_area = QScrollArea(QrHelper)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setGeometry(QRect(0, 0, 440, 300))
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName(u"scroll_widget")
        self.scroll_widget.setGeometry(QRect(0, 0, 438, 298))
        self.scroll_area.setWidget(self.scroll_widget)
        self.clear_button = QPushButton(QrHelper)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(360, 300, 80, 30))
        self.groupBox = QGroupBox(QrHelper)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(130, 300, 141, 31))
        self.groupBox.setStyleSheet(u"QGroupBox{\n"
"	border: none;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.show_pop = QRadioButton(self.groupBox)
        self.show_pop.setObjectName(u"show_pop")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.show_pop.sizePolicy().hasHeightForWidth())
        self.show_pop.setSizePolicy(sizePolicy1)
        self.show_pop.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.show_pop)

        self.show_list = QRadioButton(self.groupBox)
        self.show_list.setObjectName(u"show_list")
        sizePolicy1.setHeightForWidth(self.show_list.sizePolicy().hasHeightForWidth())
        self.show_list.setSizePolicy(sizePolicy1)
        self.show_list.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.show_list)

        self.label = QLabel(QrHelper)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(5, 300, 120, 30))

        self.retranslateUi(QrHelper)

        QMetaObject.connectSlotsByName(QrHelper)
    # setupUi

    def retranslateUi(self, QrHelper):
        QrHelper.setWindowTitle(QCoreApplication.translate("QrHelper", u"QrHelper", None))
        self.clear_button.setText(QCoreApplication.translate("QrHelper", u"Clear", None))
        self.groupBox.setTitle("")
        self.show_pop.setText(QCoreApplication.translate("QrHelper", u"Popup", None))
        self.show_list.setText(QCoreApplication.translate("QrHelper", u"List", None))
        self.label.setText(QCoreApplication.translate("QrHelper", u"Display after scanning:", None))
    # retranslateUi

