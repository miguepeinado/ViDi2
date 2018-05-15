# -*- coding: utf-8 -*-
import sys
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import dialogs
import ui_dosimetry


class DosimetryForm(ui_dosimetry.Ui_Frame, QFrame):
    NEW_RECORD = 1
    SHOW_RECORD = 2
    # Custom signals
    new_record_stored = pyqtSignal()
    record_updated = pyqtSignal(QString)
    lock_record = pyqtSignal()

    def __init__(self, db, mode=SHOW_RECORD, parent_id=None, parent=None):
        # Invoke parent's method
        super(DosimetryForm, self).__init__(parent)
        self.setupUi(self)
        # gui tweaks
        self.setLayout(self.grid_layout)
        self.tx_n_session.setVisible(False)
        self.tx_notes.setVisible(False)
        # slot/signals...
        # ...control changed
        self.old_value = None
        self.record_changed = False
        self.tx_physicist.installEventFilter(self)
        self.dt_referral.installEventFilter(self)
        self.dt_aproval.installEventFilter(self)
        self.bt_confirm.installEventFilter(self)
        # ...actions
        self.menu_widget = QPushButton(QIcon(":/database/resources/tools.svg"), "Tools")
        menu = QMenu()
        menu.addAction(self.act_edit)
        menu.addAction(self.act_undo)
        menu.addAction(self.act_notes)
        self.menu_widget.setMenu(menu)
        self.act_edit.triggered.connect(self.edit_record)
        self.act_notes.triggered.connect(self.notes)
        self.act_undo.triggered.connect(self.undo)
        self.bt_confirm.clicked.connect(self.approve_dosimetry)
        self.grid_layout.addWidget(self.menu_widget, 0, 0)
        # init values
        self.db_connect = db
        self.mode = mode
        self.record_id = -1
        # ...model with dosimetry
        self.db_connect = db
        self.dosimetry_model = QSqlTableModel(parent=None, db=self.db_connect)
        self.dosimetry_model.setTable("Dosimetries")
        self.dosimetry_model.select()
        #   ...map into form
        self.dosimetry_mapper = QDataWidgetMapper()
        self.dosimetry_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.dosimetry_mapper.setModel(self.dosimetry_model)
        self.dosimetry_mapper.addMapping(self.tx_n_session, 1)
        self.dosimetry_mapper.addMapping(self.dt_referral, 2)
        self.dosimetry_mapper.addMapping(self.tx_physicist, 3)
        self.dosimetry_mapper.addMapping(self.dt_aproval, 4)
        self.dosimetry_mapper.addMapping(self.bt_confirm, 5)
        self.dosimetry_mapper.addMapping(self.tx_notes, 6)
        if self.mode == self.NEW_RECORD:
            if parent_id is None:
                tx1 = "Database error"
                tx2 = "Wrong ID link between tree and form"
                QMessageBox.critical(self, tx1, tx2)
                logging.error(tx1 + ": " + tx2)
                sys.exit(1)
            logging.info("new dosimetry in db. Fill data...")
            row = self.dosimetry_model.rowCount()
            self.dosimetry_model.insertRow(row)
            self.dosimetry_mapper.setCurrentIndex(row)
            self.tx_n_session.setText(parent_id)
            self.dt_referral.setDate(QDate.currentDate())
            self.act_edit.trigger()

    def approve_dosimetry(self, is_checked):
            self.record_changed = True
            logging.info("approve dosimetry record (id={})".format(self.record_id))
            if is_checked:
                self.dt_aproval.setDate(QDate.currentDate())

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
        self.tx_physicist.setEnabled(enabled)
        self.bt_confirm.setEnabled(enabled)
        self.dt_referral.setEnabled(enabled)
        self.dt_aproval.setEnabled(enabled)
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
            elif type(o2) == QDateEdit or type(o2) == QDateTimeEdit:
                return o2.date()
            else:  # QPushButton:
                return o2.isChecked()

        if evt.type() == QEvent.FocusIn:
            self.old_value = get_value(o)
        elif evt.type() == QEvent.FocusOut:
            self.record_changed |= (self.old_value != get_value(o))
            if self.record_changed:
                logging.info("record ({}) has changed".format(self.record_id))
        return False

    def notes(self):
        dlg = dialogs.Notes("Dosimetry notes", self.tx_notes.toPlainText())
        if dlg.exec_() == dlg.Accepted:
            self.tx_notes.clear()
            self.tx_notes.appendPlainText(dlg.tx_plain.toPlainText())
            self.dosimetry_mapper.submit()

    def submit_record(self):
        # ...update record
        if not self.record_changed:
            return False
        if not self.dosimetry_mapper.submit():
            logging.error("\tError managing dosimetry record..." + self.dosimetry_model.lastError().text())
            QMessageBox.critical(self, "Update database",
                                 "Error managing dosimetry record..." + self.dosimetry_model.lastError().text())
            return False
        else:
            logging.info("\tDosimetry (id={}) record stored: OK".format(self.record_id))
        if self.mode == self.NEW_RECORD:
            q = self.dosimetry_model.query()
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
            self.dosimetry_mapper.toFirst()
        self.act_edit.setChecked(False)
        self.enable_fields(False)
        self.act_edit.setText("Edit")

    def update_form(self, session_key, is_locked):
        self.record_id = session_key
        self.mode = self.SHOW_RECORD
        self.enable_fields(False)
        self.dosimetry_model.setFilter("ID={}".format(session_key))
        self.dosimetry_model.select()
        row = self.dosimetry_model.rowCount()
        if row == 0:
            tx1 = "Database error"
            tx2 = "Wrong ID link between tree and form"
            QMessageBox.critical(self, tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        elif row > 1:
            tx1 = "Database error"
            tx2 = "Two dosimetries records with the same ID"
            QMessageBox.critical(self, tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        self.dosimetry_mapper.toFirst()
        self.menu_widget.setVisible(not is_locked)


    def __str__(self):
        s = "Dosimetry"
        s += ": approved by " + str(self.tx_physicist.text()) if self.bt_confirm.isChecked() else ""
        return s