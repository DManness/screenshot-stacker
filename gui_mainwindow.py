# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 540)
        MainWindow.setMinimumSize(QSize(636, 402))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(300, 300))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 578, 448))
        self.horizontalLayout_4 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.img_preview = QLabel(self.scrollAreaWidgetContents)
        self.img_preview.setObjectName(u"img_preview")
        self.img_preview.setMinimumSize(QSize(0, 0))
        self.img_preview.setContextMenuPolicy(Qt.NoContextMenu)
        self.img_preview.setTextFormat(Qt.PlainText)

        self.horizontalLayout_4.addWidget(self.img_preview)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox1 = QGroupBox(self.centralwidget)
        self.groupBox1.setObjectName(u"groupBox1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox1.sizePolicy().hasHeightForWidth())
        self.groupBox1.setSizePolicy(sizePolicy1)
        self.formLayout = QFormLayout(self.groupBox1)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox1)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label)

        self.widget = QWidget(self.groupBox1)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.opt_orientation_vertical = QRadioButton(self.widget)
        self.opt_orientation_vertical.setObjectName(u"opt_orientation_vertical")
        self.opt_orientation_vertical.setMinimumSize(QSize(0, 0))
        self.opt_orientation_vertical.setContextMenuPolicy(Qt.NoContextMenu)
        self.opt_orientation_vertical.setChecked(True)

        self.horizontalLayout.addWidget(self.opt_orientation_vertical)

        self.opt_orientation_horizontal = QRadioButton(self.widget)
        self.opt_orientation_horizontal.setObjectName(u"opt_orientation_horizontal")

        self.horizontalLayout.addWidget(self.opt_orientation_horizontal)


        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.widget)

        self.label_2 = QLabel(self.groupBox1)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, -1, -1, 0)
        self.btn_img_move_up = QPushButton(self.groupBox1)
        self.btn_img_move_up.setObjectName(u"btn_img_move_up")
        sizePolicy3 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_img_move_up.sizePolicy().hasHeightForWidth())
        self.btn_img_move_up.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.btn_img_move_up, 1, 3, 1, 1)

        self.btn_img_move_down = QPushButton(self.groupBox1)
        self.btn_img_move_down.setObjectName(u"btn_img_move_down")
        sizePolicy3.setHeightForWidth(self.btn_img_move_down.sizePolicy().hasHeightForWidth())
        self.btn_img_move_down.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.btn_img_move_down, 1, 2, 1, 1)

        self.btn_img_remove = QPushButton(self.groupBox1)
        self.btn_img_remove.setObjectName(u"btn_img_remove")
        sizePolicy3.setHeightForWidth(self.btn_img_remove.sizePolicy().hasHeightForWidth())
        self.btn_img_remove.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.btn_img_remove, 1, 1, 1, 1)

        self.btn_img_add = QPushButton(self.groupBox1)
        self.btn_img_add.setObjectName(u"btn_img_add")
        sizePolicy4 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_img_add.sizePolicy().hasHeightForWidth())
        self.btn_img_add.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.btn_img_add, 1, 0, 1, 1)

        self.lst_file_list = QListView(self.groupBox1)
        self.lst_file_list.setObjectName(u"lst_file_list")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lst_file_list.sizePolicy().hasHeightForWidth())
        self.lst_file_list.setSizePolicy(sizePolicy5)

        self.gridLayout_2.addWidget(self.lst_file_list, 0, 0, 1, 4)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.gridLayout_2)

        self.label_3 = QLabel(self.groupBox1)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_3)

        self.widget_2 = QWidget(self.groupBox1)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txt_save_as_path = QLineEdit(self.widget_2)
        self.txt_save_as_path.setObjectName(u"txt_save_as_path")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.txt_save_as_path.sizePolicy().hasHeightForWidth())
        self.txt_save_as_path.setSizePolicy(sizePolicy6)

        self.horizontalLayout_2.addWidget(self.txt_save_as_path)

        self.btn_save_as_browse = QPushButton(self.widget_2)
        self.btn_save_as_browse.setObjectName(u"btn_save_as_browse")

        self.horizontalLayout_2.addWidget(self.btn_save_as_browse)


        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.widget_2)

        self.widget_3 = QWidget(self.groupBox1)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btn_preview = QPushButton(self.widget_3)
        self.btn_preview.setObjectName(u"btn_preview")

        self.horizontalLayout_3.addWidget(self.btn_preview)

        self.btn_export = QPushButton(self.widget_3)
        self.btn_export.setObjectName(u"btn_export")

        self.horizontalLayout_3.addWidget(self.btn_export)


        self.formLayout.setWidget(9, QFormLayout.SpanningRole, self.widget_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(6, QFormLayout.LabelRole, self.verticalSpacer)

        self.label_4 = QLabel(self.groupBox1)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_4)

        self.widget_4 = QWidget(self.groupBox1)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.opt_align_left = QRadioButton(self.widget_4)
        self.opt_align_left.setObjectName(u"opt_align_left")
        self.opt_align_left.setChecked(True)

        self.horizontalLayout_5.addWidget(self.opt_align_left)

        self.opt_align_center = QRadioButton(self.widget_4)
        self.opt_align_center.setObjectName(u"opt_align_center")

        self.horizontalLayout_5.addWidget(self.opt_align_center)

        self.opt_align_right = QRadioButton(self.widget_4)
        self.opt_align_right.setObjectName(u"opt_align_right")

        self.horizontalLayout_5.addWidget(self.opt_align_right)


        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.widget_4)


        self.gridLayout.addWidget(self.groupBox1, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Screenshot Stacker", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.img_preview.setText("")
        self.groupBox1.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Orientation", None))
        self.opt_orientation_vertical.setText(QCoreApplication.translate("MainWindow", u"Vertical", None))
        self.opt_orientation_horizontal.setText(QCoreApplication.translate("MainWindow", u"Horizontal", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Layout", None))
        self.btn_img_move_up.setText(QCoreApplication.translate("MainWindow", u"Up", None))
        self.btn_img_move_down.setText(QCoreApplication.translate("MainWindow", u"Down", None))
        self.btn_img_remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.btn_img_add.setText(QCoreApplication.translate("MainWindow", u"Add...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.btn_save_as_browse.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.btn_preview.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.btn_export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Alignment", None))
        self.opt_align_left.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.opt_align_center.setText(QCoreApplication.translate("MainWindow", u"Center", None))
        self.opt_align_right.setText(QCoreApplication.translate("MainWindow", u"Right", None))
    # retranslateUi

