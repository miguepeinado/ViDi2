# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/resources/ViDi.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.dock_widget = QtGui.QDockWidget(self.centralwidget)
        self.dock_widget.setGeometry(QtCore.QRect(0, 0, 318, 630))
        self.dock_widget.setMinimumSize(QtCore.QSize(318, 41))
        self.dock_widget.setMaximumSize(QtCore.QSize(518, 524287))
        self.dock_widget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dock_widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dock_widget.setObjectName(_fromUtf8("dock_widget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.dock_widget.setWidget(self.dockWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtGui.QStatusBar(MainWindow)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ViDi", None))

import icons_rc
