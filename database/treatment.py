import sys
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import dialogs
import ui_treatment


class TreatmentForm(ui_treatment.Ui_Frame, QFrame):

    NEW_RECORD = 1
    SHOW_RECORD = 2
    # Custom signals
    new_record_stored = pyqtSignal()
    record_updated = pyqtSignal(QString)
    lock_record = pyqtSignal()

    def __init__(self, db, mode=SHOW_RECORD, parent_id=None, parent=None):
        # Invoke parent's method
        super(TreatmentForm, self).__init__(parent)
        self.setupUi(self)
        # gui tweaks
        self.setLayout(self.grid_layout)
        self.tx_n_patient.setVisible(False)
        self.ck_locked.setVisible(False)
        self.tx_notes.setVisible(False)
        # slot/signals...
        # ...control changed
        self.old_value = None
        self.record_changed = False
        self.dt_start_date.installEventFilter(self)
        self.dt_end_date.installEventFilter(self)
        self.tx_physician.installEventFilter(self)
        self.tx_diagnostic.installEventFilter(self)
        self.tx_schedule.installEventFilter(self)
        self.tx_pharmaceutical.installEventFilter(self)
        # ...actions
        self.menu_widget = QPushButton(QIcon(":/database/resources/tools.svg"), "Tools")
        menu = QMenu()
        menu.addAction(self.act_edit)
        menu.addAction(self.act_undo)
        menu.addAction(self.act_notes)
        menu.addAction(self.act_lock)
        self.menu_widget.setMenu(menu)
        self.act_edit.triggered.connect(self.edit_record)
        self.act_notes.triggered.connect(self.notes)
        self.act_undo.triggered.connect(self.undo)
        self.act_lock.triggered.connect(self.end_treatment)
        self.grid_layout.addWidget(self.menu_widget, 0, 0)
        # init values
        self.db_connect = db
        self.mode = mode
        self.record_id = -1
        # ...model with treatment
        self.treatment_model = QSqlTableModel(parent=None, db=self.db_connect)
        self.treatment_model.setTable("Treatments")
        self.treatment_model.select()
        #   ...map into form
        self.treatment_mapper = QDataWidgetMapper()
        self.treatment_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.treatment_mapper.setModel(self.treatment_model)
        self.treatment_mapper.addMapping(self.tx_n_patient, 1)
        self.treatment_mapper.addMapping(self.tx_diagnostic, 2)
        self.treatment_mapper.addMapping(self.tx_physician, 3)
        self.treatment_mapper.addMapping(self.dt_start_date, 4)
        self.treatment_mapper.addMapping(self.tx_schedule, 5)
        self.treatment_mapper.addMapping(self.tx_pharmaceutical, 6)
        self.treatment_mapper.addMapping(self.dt_end_date, 7)
        self.treatment_mapper.addMapping(self.ck_locked, 8)
        self.treatment_mapper.addMapping(self.tx_notes, 9)
        if self.mode == self.NEW_RECORD:
            if parent_id is None:
                tx1 = "Database error"
                tx2 = "Wrong ID link between tree and form"
                QMessageBox.critical(self, tx1, tx2)
                logging.error(tx1 + ": " + tx2)
                sys.exit(1)
            logging.info("new treatment in db. Fill data...")
            row = self.treatment_model.rowCount()
            self.treatment_model.insertRow(row)
            self.treatment_mapper.setCurrentIndex(row)
            self.tx_n_patient.setText(parent_id)
            self.dt_start_date.setDate(QDate.currentDate())
            self.act_edit.trigger()

    def edit_record(self):
            if self.act_edit.isChecked():
                self.enable_fields(True)
                self.act_edit.setText("Update")
            else:
                # Submit record?
                if self.record_changed:
                    if QMessageBox.question(self, "Update database", "Record will be updated. Apply changes?",
                                            QMessageBox.Apply | QMessageBox.Cancel) != QMessageBox.Apply:
                        self.act_edit.setChecked(True)
                        return
                    if self.submit_record():
                        self.enable_fields(False)
                        self.act_edit.setText("Edit")
                        txt = str(self)
                        self.record_updated.emit(txt)
                else:
                    self.act_edit.setChecked(True)

    def enable_fields(self, enabled):
        self.dt_start_date.setEnabled(enabled)
        self.dt_end_date.setEnabled(enabled)
        self.tx_physician.setEnabled(enabled)
        self.tx_diagnostic.setEnabled(enabled)
        self.tx_schedule.setEnabled(enabled)
        self.tx_pharmaceutical.setEnabled(enabled)
        self.act_undo.setEnabled(enabled)

    def end_treatment(self):
        if QMessageBox.question(self, "Update database",
                                     "This action will end the treatment\n"
                                     "and block all the pending data. Continue?",
                                     QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
            self.ck_locked.setChecked(True)
            self.record_changed = True
            self.submit_record()
            logging.info("lock treatment record (id={})".format(self.record_id))
            self.menu_widget.setVisible(False)
            self.lock_record.emit()

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
            else:  # QComboBox:
                return o2.currentIndex()

        if evt.type() == QEvent.FocusIn:
            self.old_value = get_value(o)
        elif evt.type() == QEvent.FocusOut:
            self.record_changed |= (self.old_value != get_value(o))
            if self.record_changed:
                logging.info("record ({}) has changed".format(self.record_id))
        return False

    def notes(self):
        dlg = dialogs.Notes("Treatment notes", self.tx_notes.toPlainText())
        if dlg.exec_() == dlg.Accepted:
            self.tx_notes.clear()
            self.tx_notes.appendPlainText(dlg.tx_plain.toPlainText())
            self.submit_record()

    def submit_record(self):
        # ...update record
        if not self.record_changed:
            return False
        if not self.treatment_mapper.submit():
            logging.error("\tError managing treatment record..." + self.treatment_model.lastError().text())
            QMessageBox.critical(self, "Update database",
                                 "Error managing treatment record..." + self.treatment_model.lastError().text())
            return False
        else:
            logging.info("\tTreatment (id={}) record stored: OK".format(self.record_id))
        if self.mode == self.NEW_RECORD:
            q = self.treatment_model.query()
            q.last()
            self.record_id, _ = q.value(0).toInt()
            self.new_record_stored.emit()
        self.record_changed = False
        return True

    def undo(self):
        if self.record_changed:
            if QMessageBox.question(self, "Update database", "Record has changed. Discard all changes?",
                                    QMessageBox.Cancel | QMessageBox.Discard) == QMessageBox.Cancel:
                return
            self.treatment_mapper.toFirst()
        self.act_edit.setChecked(False)
        self.enable_fields(False)
        self.act_edit.setText("Edit")

    def update_form(self, treatment_key, is_locked):
        self.record_id = treatment_key
        self.mode = self.SHOW_RECORD
        self.enable_fields(False)
        self.treatment_model.setFilter("ID={}".format(treatment_key))
        self.treatment_model.select()
        row = self.treatment_model.rowCount()
        if row == 0:
            tx1 = "Database error"
            tx2 = "Wrong ID link between tree and form"
            QMessageBox.critical(self, tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        elif row > 1:
            tx1 = "Database error"
            tx2 = "Two treatment records with the same ID"
            QMessageBox.critical(self, tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        self.treatment_mapper.toFirst()
        self.menu_widget.setVisible(not is_locked)

    def __str__(self):
        tx = self.tx_pharmaceutical.text()
        tx += " (" + self.tx_schedule.text() + ")" if len(self.tx_schedule.text()) > 0 else ""
        s = str(tx)
        return s