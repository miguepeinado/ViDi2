# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patient.ui'
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

class Ui_Patient(object):
    def setupUi(self, Patient):
        Patient.setObjectName(_fromUtf8("Patient"))
        Patient.resize(429, 424)
        Patient.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Patient.setFrameShape(QtGui.QFrame.StyledPanel)
        Patient.setFrameShadow(QtGui.QFrame.Raised)
        self.layoutWidget = QtGui.QWidget(Patient)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 20, 421, 364))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.grid_layout = QtGui.QGridLayout(self.layoutWidget)
        self.grid_layout.setMargin(10)
        self.grid_layout.setObjectName(_fromUtf8("grid_layout"))
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.grid_layout.addWidget(self.label_6, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.grid_layout.addWidget(self.label, 1, 0, 1, 1)
        self.tx_weight = QtGui.QLineEdit(self.layoutWidget)
        self.tx_weight.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_weight.sizePolicy().hasHeightForWidth())
        self.tx_weight.setSizePolicy(sizePolicy)
        self.tx_weight.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tx_weight.setObjectName(_fromUtf8("tx_weight"))
        self.grid_layout.addWidget(self.tx_weight, 3, 1, 1, 1)
        self.tx_age = QtGui.QLineEdit(self.layoutWidget)
        self.tx_age.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_age.sizePolicy().hasHeightForWidth())
        self.tx_age.setSizePolicy(sizePolicy)
        self.tx_age.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tx_age.setObjectName(_fromUtf8("tx_age"))
        self.grid_layout.addWidget(self.tx_age, 2, 4, 1, 1)
        self.tx_name = QtGui.QLineEdit(self.layoutWidget)
        self.tx_name.setEnabled(True)
        self.tx_name.setObjectName(_fromUtf8("tx_name"))
        self.grid_layout.addWidget(self.tx_name, 1, 1, 1, 4)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.grid_layout.addWidget(self.label_4, 2, 3, 1, 1)
        self.dt_birth_date = QtGui.QDateEdit(self.layoutWidget)
        self.dt_birth_date.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dt_birth_date.sizePolicy().hasHeightForWidth())
        self.dt_birth_date.setSizePolicy(sizePolicy)
        self.dt_birth_date.setMaximumSize(QtCore.QSize(120, 16777215))
        self.dt_birth_date.setFrame(True)
        self.dt_birth_date.setCalendarPopup(True)
        self.dt_birth_date.setObjectName(_fromUtf8("dt_birth_date"))
        self.grid_layout.addWidget(self.dt_birth_date, 2, 1, 1, 2)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.grid_layout.addWidget(self.label_2, 0, 1, 1, 1)
        self.tx_notes = QtGui.QPlainTextEdit(self.layoutWidget)
        self.tx_notes.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tx_notes.setObjectName(_fromUtf8("tx_notes"))
        self.grid_layout.addWidget(self.tx_notes, 4, 0, 1, 5)
        self.tx_id = QtGui.QLineEdit(self.layoutWidget)
        self.tx_id.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_id.sizePolicy().hasHeightForWidth())
        self.tx_id.setSizePolicy(sizePolicy)
        self.tx_id.setMaximumSize(QtCore.QSize(150, 16777215))
        self.tx_id.setObjectName(_fromUtf8("tx_id"))
        self.grid_layout.addWidget(self.tx_id, 0, 2, 1, 3)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.grid_layout.addWidget(self.label_3, 2, 0, 1, 1)
        self.cb_sex = QtGui.QComboBox(self.layoutWidget)
        self.cb_sex.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_sex.sizePolicy().hasHeightForWidth())
        self.cb_sex.setSizePolicy(sizePolicy)
        self.cb_sex.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cb_sex.setObjectName(_fromUtf8("cb_sex"))
        self.cb_sex.addItem(_fromUtf8(""))
        self.cb_sex.addItem(_fromUtf8(""))
        self.cb_sex.addItem(_fromUtf8(""))
        self.grid_layout.addWidget(self.cb_sex, 3, 4, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.grid_layout.addWidget(self.label_5, 3, 3, 1, 1)
        self.act_edit = QtGui.QAction(Patient)
        self.act_edit.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/edit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_edit.setIcon(icon)
        self.act_edit.setObjectName(_fromUtf8("act_edit"))
        self.act_undo = QtGui.QAction(Patient)
        self.act_undo.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/undo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_undo.setIcon(icon1)
        self.act_undo.setObjectName(_fromUtf8("act_undo"))
        self.act_notes = QtGui.QAction(Patient)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/database/resources/notas.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_notes.setIcon(icon2)
        self.act_notes.setObjectName(_fromUtf8("act_notes"))
        self.label_6.setBuddy(self.tx_weight)
        self.label.setBuddy(self.tx_name)
        self.label_4.setBuddy(self.tx_age)
        self.label_2.setBuddy(self.tx_id)
        self.label_3.setBuddy(self.dt_birth_date)
        self.label_5.setBuddy(self.cb_sex)

        self.retranslateUi(Patient)
        QtCore.QMetaObject.connectSlotsByName(Patient)
        Patient.setTabOrder(self.tx_name, self.dt_birth_date)
        Patient.setTabOrder(self.dt_birth_date, self.tx_age)
        Patient.setTabOrder(self.tx_age, self.tx_weight)
        Patient.setTabOrder(self.tx_weight, self.tx_notes)

    def retranslateUi(self, Patient):
        Patient.setWindowTitle(_translate("Patient", "Frame", None))
        self.label_6.setText(_translate("Patient", "Weight  (kg):", None))
        self.label.setText(_translate("Patient", "Name:", None))
        self.label_4.setText(_translate("Patient", "Age:", None))
        self.dt_birth_date.setDisplayFormat(_translate("Patient", "dd/MM/yyyy", None))
        self.label_2.setText(_translate("Patient", "ID:", None))
        self.label_3.setText(_translate("Patient", "Birth date:", None))
        self.cb_sex.setItemText(0, _translate("Patient", "Female", None))
        self.cb_sex.setItemText(1, _translate("Patient", "Male", None))
        self.cb_sex.setItemText(2, _translate("Patient", "Other", None))
        self.label_5.setText(_translate("Patient", "sex:", None))
        self.act_edit.setText(_translate("Patient", "Edit/Update", None))
        self.act_edit.setToolTip(_translate("Patient", "Edit/Update record", None))
        self.act_undo.setText(_translate("Patient", "Undo", None))
        self.act_undo.setToolTip(_translate("Patient", "Undo edition and lock record", None))
        self.act_notes.setText(_translate("Patient", "Notes", None))

import icons_rc
