# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dosimetry.ui'
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

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(438, 235)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setMinimumSize(QtCore.QSize(0, 0))
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayoutWidget = QtGui.QWidget(Frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 245))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.grid_layout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.grid_layout.setMargin(10)
        self.grid_layout.setObjectName(_fromUtf8("grid_layout"))
        self.bt_confirm = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_confirm.sizePolicy().hasHeightForWidth())
        self.bt_confirm.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/confirm.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_confirm.setIcon(icon)
        self.bt_confirm.setCheckable(True)
        self.bt_confirm.setObjectName(_fromUtf8("bt_confirm"))
        self.grid_layout.addWidget(self.bt_confirm, 3, 3, 1, 2)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.grid_layout.addWidget(self.label_3, 2, 0, 1, 1)
        self.dt_referral = QtGui.QDateEdit(self.gridLayoutWidget)
        self.dt_referral.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dt_referral.sizePolicy().hasHeightForWidth())
        self.dt_referral.setSizePolicy(sizePolicy)
        self.dt_referral.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.dt_referral.setCalendarPopup(True)
        self.dt_referral.setObjectName(_fromUtf8("dt_referral"))
        self.grid_layout.addWidget(self.dt_referral, 2, 1, 1, 2)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.grid_layout.addWidget(self.label, 3, 0, 1, 1)
        self.dt_aproval = QtGui.QDateEdit(self.gridLayoutWidget)
        self.dt_aproval.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dt_aproval.sizePolicy().hasHeightForWidth())
        self.dt_aproval.setSizePolicy(sizePolicy)
        self.dt_aproval.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.dt_aproval.setCalendarPopup(True)
        self.dt_aproval.setObjectName(_fromUtf8("dt_aproval"))
        self.grid_layout.addWidget(self.dt_aproval, 3, 1, 1, 2)
        self.bt_calculate = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_calculate.sizePolicy().hasHeightForWidth())
        self.bt_calculate.setSizePolicy(sizePolicy)
        self.bt_calculate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/calculator.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_calculate.setIcon(icon1)
        self.bt_calculate.setIconSize(QtCore.QSize(24, 24))
        self.bt_calculate.setObjectName(_fromUtf8("bt_calculate"))
        self.grid_layout.addWidget(self.bt_calculate, 2, 3, 1, 2)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.grid_layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.tx_n_session = QtGui.QLineEdit(self.gridLayoutWidget)
        self.tx_n_session.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_n_session.sizePolicy().hasHeightForWidth())
        self.tx_n_session.setSizePolicy(sizePolicy)
        self.tx_n_session.setMaximumSize(QtCore.QSize(40, 16777215))
        self.tx_n_session.setObjectName(_fromUtf8("tx_n_session"))
        self.grid_layout.addWidget(self.tx_n_session, 0, 2, 1, 1)
        self.tx_physicist = QtGui.QLineEdit(self.gridLayoutWidget)
        self.tx_physicist.setObjectName(_fromUtf8("tx_physicist"))
        self.grid_layout.addWidget(self.tx_physicist, 1, 1, 1, 4)
        self.tx_notes = QtGui.QPlainTextEdit(self.gridLayoutWidget)
        self.tx_notes.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tx_notes.setObjectName(_fromUtf8("tx_notes"))
        self.grid_layout.addWidget(self.tx_notes, 4, 0, 1, 5)
        self.act_edit = QtGui.QAction(Frame)
        self.act_edit.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/edit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_edit.setIcon(icon2)
        self.act_edit.setObjectName(_fromUtf8("act_edit"))
        self.act_undo = QtGui.QAction(Frame)
        self.act_undo.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/undo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_undo.setIcon(icon3)
        self.act_undo.setObjectName(_fromUtf8("act_undo"))
        self.act_notes = QtGui.QAction(Frame)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/notas.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_notes.setIcon(icon4)
        self.act_notes.setObjectName(_fromUtf8("act_notes"))

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.bt_confirm.setText(_translate("Frame", "Confirm", None))
        self.label_3.setText(_translate("Frame", "Date referral", None))
        self.label.setText(_translate("Frame", "Date Aproval", None))
        self.bt_calculate.setToolTip(_translate("Frame", "Calculate organ doses", None))
        self.bt_calculate.setText(_translate("Frame", "Calculate", None))
        self.label_2.setText(_translate("Frame", "Physicist", None))
        self.act_edit.setText(_translate("Frame", "Edit/Update", None))
        self.act_edit.setToolTip(_translate("Frame", "Edit/Update record", None))
        self.act_undo.setText(_translate("Frame", "Undo", None))
        self.act_undo.setToolTip(_translate("Frame", "Undo edition and lock record", None))
        self.act_notes.setText(_translate("Frame", "Notes", None))

import icons_rc
