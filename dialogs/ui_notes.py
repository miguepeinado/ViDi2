# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notes.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(346, 167)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/notas.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 321, 131))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.grid_layout = QtGui.QGridLayout(self.layoutWidget)
        self.grid_layout.setMargin(10)
        self.grid_layout.setObjectName(_fromUtf8("grid_layout"))
        self.bt_clear_text = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_clear_text.sizePolicy().hasHeightForWidth())
        self.bt_clear_text.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/undo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_clear_text.setIcon(icon1)
        self.bt_clear_text.setIconSize(QtCore.QSize(24, 24))
        self.bt_clear_text.setObjectName(_fromUtf8("bt_clear_text"))
        self.grid_layout.addWidget(self.bt_clear_text, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.grid_layout.addItem(spacerItem, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.grid_layout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.tx_plain = QtGui.QPlainTextEdit(self.layoutWidget)
        self.tx_plain.setObjectName(_fromUtf8("tx_plain"))
        self.grid_layout.addWidget(self.tx_plain, 0, 0, 2, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.bt_clear_text.setText(_translate("Dialog", "clear", None))

import icons_rc
