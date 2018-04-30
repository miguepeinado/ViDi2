import logging
import sys
import dialogs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import ui_patient


class PatientForm(ui_patient.Ui_Patient, QFrame):
    NEW_RECORD = 1
    SHOW_RECORD = 2
    new_record_stored = pyqtSignal()
    record_updated = pyqtSignal(QString)

    def __init__(self, db, mode=SHOW_RECORD, patient_id=None, parent=None):
        # Invoke parent's method
        super(PatientForm, self).__init__(parent)
        self.setupUi(self)
        # gui tweaks
        self.setLayout(self.grid_layout)
        self.tx_notes.setVisible(False)
        # slot/signals...
        # ...control changed
        self.old_value = None
        self.record_changed = False
        self.tx_id.installEventFilter(self)
        self.tx_name.installEventFilter(self)
        self.dt_birth_date.installEventFilter(self)
        self.tx_age.installEventFilter(self)
        self.tx_weight.installEventFilter(self)
        self.cb_sex.installEventFilter(self)
        # ...actions
        menu_widget = QPushButton("Tools")
        menu = QMenu()
        menu.addAction(self.act_edit)
        menu.addAction(self.act_undo)
        menu.addAction(self.act_notes)
        menu_widget.setMenu(menu)
        self.act_edit.triggered.connect(self.edit_record)
        self.act_notes.triggered.connect(self.notes)
        self.act_undo.triggered.connect(self.undo)
        self.grid_layout.addWidget(menu_widget, 0, 0)
        # init values
        self.db_connect = db
        self.mode = mode
        # Data base issues...
        # ...model with patient
        self.patient_model = QSqlTableModel(parent=None, db=self.db_connect)
        self.patient_model.setTable("Patients")
        self.patient_model.select()
        #   ...map into widgets
        self.patient_mapper = QDataWidgetMapper()
        self.patient_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.patient_mapper.setModel(self.patient_model)
        self.patient_mapper.addMapping(self.tx_name, 1)
        self.patient_mapper.addMapping(self.tx_id, 0)
        self.patient_mapper.addMapping(self.dt_birth_date, 2)
        self.patient_mapper.addMapping(self.tx_age, 3)
        self.patient_mapper.addMapping(self.cb_sex, 4, "currentIndex")
        self.patient_mapper.addMapping(self.tx_weight, 5)
        self.patient_mapper.addMapping(self.tx_notes, 6)
        if self.mode == self.NEW_RECORD:
            logging.info("new patient in db. Fill data...")
            row = self.patient_model.rowCount()
            self.patient_model.insertRow(row)
            self.patient_mapper.setCurrentIndex(row)
            self.tx_id.setEnabled(True)
            self.act_edit.trigger()
        else:
            logging.info("patient data already in db...update treatment form")

    def edit_record(self):
        if self.act_edit.isChecked():
            self.enable_fields(True)
            self.act_edit.setText("Update")
        else:
            # Submit record?
            if self.record_changed and len(self.tx_id.text()) > 0:
                if QMessageBox.question(self, "Update database", "Record will be updated. Apply changes?",
                                        QMessageBox.Apply | QMessageBox.Cancel) != QMessageBox.Apply:
                    self.act_edit.setChecked(True)
                    return
            if self.submit_record():
                self.enable_fields(False)
                self.act_edit.setText("Edit")

    def enable_fields(self, enabled):
        self.tx_name.setEnabled(enabled)
        self.dt_birth_date.setEnabled(enabled)
        self.tx_age.setEnabled(enabled)
        self.cb_sex.setEnabled(enabled)
        self.tx_weight.setEnabled(enabled)
        self.act_undo.setEnabled(enabled)

    def eventFilter(self, o, evt):
        """
        Manage if some record has been changed
        :param o: The source(QObject) of the event
        :param evt: The event(QEvent) raised
        :return: View docs for True/False meaning
        """
        def get_value(o2):
            if type(o2) == QLineEdit:
                return o2.text()
            elif type(o2) == QDateEdit:
                return o2.date()
            else:         # QComboBox:
                return o2.currentIndex()

        if evt.type() == QEvent.FocusIn:
            self.old_value = get_value(o)
            # print self.old_value
        elif evt.type() == QEvent.FocusOut:
            self.record_changed = (self.old_value != get_value(o))
            logging.info("record ({}) has changed".format(self.tx_id.text()))
        return False

    def notes(self):
        dlg = dialogs.Notes("Patient notes", self.tx_notes.toPlainText())
        if dlg.exec_() == dlg.Accepted:
            self.tx_notes.clear()
            self.tx_notes.appendPlainText(dlg.tx_plain.toPlainText())
            self.submit_record()

    def submit_record(self):
        # ...update record
        if not self.patient_mapper.submit():
            logging.error("\tError managing patient record..." + self.patient_model.lastError().text())
            QMessageBox.critical(self, "Update database",
                                 "Error managing patient record..." + self.patient_model.lastError().text())
            return False
        else:
            logging.info("\tPatient (id={}) new record stored: OK".format(self.tx_id.text()))
        if self.mode == self.NEW_RECORD:
            self.new_record_stored.emit()
        self.record_changed = False
        return True

    def undo(self):
        if self.record_changed:
            if QMessageBox.question(self, "Update database", "Record has changed. Discard all changes?",
                                    QMessageBox.Cancel | QMessageBox.Discard) == QMessageBox.Cancel:
                return
            self.patient_mapper.toFirst()
        self.act_edit.setChecked(False)
        self.enable_fields(False)
        self.act_edit.setText("Edit")

    def update_form(self, patient_key):
        self.mode = self.SHOW_RECORD
        self.tx_id.setEnabled(False)
        self.enable_fields(False)
        self.patient_model.setFilter("ID='{}'".format(patient_key))
        self.patient_model.select()
        row = self.patient_model.rowCount()
        if row == 0:
            tx1 = "Database error"
            tx2 = "Wrong ID link between tree and form"
            QMessageBox.critical(tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        elif row > 1:
            tx1 = "Database error"
            tx2 = "Two patient records with the same ID"
            QMessageBox.critical(tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        self.patient_mapper.toFirst()

    def __str__(self):
        s = str(self.tx_name.text()) + " (" + str(self.tx_id.text()) + ")"
        return s