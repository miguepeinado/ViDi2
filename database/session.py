# -*- coding: utf-8 -*-
import sys
import logging
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import dialogs
import ui_session


class SessionForm(ui_session.Ui_Frame, QFrame):
    NEW_RECORD = 1
    SHOW_RECORD = 2
    # Custom signals
    new_record_stored = pyqtSignal()
    record_updated = pyqtSignal(QString)
    lock_record = pyqtSignal()

    def __init__(self, db, mode=SHOW_RECORD, parent_id=None, session_number=1, parent=None):
        # Invoke parent's method
        super(SessionForm, self).__init__(parent)
        self.setupUi(self)
        # gui tweaks
        self.setLayout(self.grid_layout)
        self.tx_n_treatment.setVisible(False)
        self.ck_locked.setVisible(False)
        self.tx_notes.setVisible(False)
        # slot/signals...
        # ...control changed
        self.old_value = None
        self.record_changed = False
        self.sp_session.installEventFilter(self)
        self.tx_isotope.installEventFilter(self)
        self.sp_activity.installEventFilter(self)
        self.dt_admin.installEventFilter(self)
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
        self.act_lock.triggered.connect(self.end_session)
        self.grid_layout.addWidget(self.menu_widget, 0, 0)
        # init values
        self.db_connect = db
        self.mode = mode
        self.record_id = -1
        # ...model with session
        self.db_connect = db
        self.session_model = QSqlTableModel(parent=None, db=self.db_connect)
        self.session_model.setTable("Sessions")
        self.session_model.select()
        #   ...map into form
        self.session_mapper = QDataWidgetMapper()
        self.session_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.session_mapper.setModel(self.session_model)
        self.session_mapper.addMapping(self.tx_n_treatment, 1)
        self.session_mapper.addMapping(self.sp_session, 2)
        self.session_mapper.addMapping(self.sp_activity, 3)
        self.session_mapper.addMapping(self.tx_isotope, 4)
        self.session_mapper.addMapping(self.dt_admin, 5)
        self.session_mapper.addMapping(self.ck_locked, 6)
        self.session_mapper.addMapping(self.tx_notes, 7)
        if self.mode == self.NEW_RECORD:
            if parent_id is None:
                tx1 = "Database error"
                tx2 = "Wrong ID link between tree and form"
                QMessageBox.critical(self, tx1, tx2)
                logging.error(tx1 + ": " + tx2)
                sys.exit(1)
            logging.info("new session in db. Fill data...")
            row = self.session_model.rowCount()
            self.session_model.insertRow(row)
            self.session_mapper.setCurrentIndex(row)
            self.tx_n_treatment.setText(parent_id)
            self.sp_session.setValue(session_number)
            self.dt_admin.setDateTime(QDateTime.currentDateTime())
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
        self.sp_session.setEnabled(enabled)
        self.sp_activity.setEnabled(enabled)
        self.tx_isotope.setEnabled(enabled)
        self.dt_admin.setEnabled(enabled)
        self.act_undo.setEnabled(enabled)

    def end_session(self):
        if QMessageBox.question(self, "Update database",
                                     "This action will end the session\n"
                                     "and block all the pending data. Continue?",
                                     QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
            self.ck_locked.setChecked(True)
            self.record_changed = True
            self.submit_record()
            logging.info("lock session record (id={})".format(self.record_id))
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
            elif type(o2) == QDateEdit or type(o2) == QDateTimeEdit:
                return o2.date()
            else:  # QSpinBox:
                return o2.value()

        if evt.type() == QEvent.FocusIn:
            self.old_value = get_value(o)
        elif evt.type() == QEvent.FocusOut:
            self.record_changed = (self.old_value != get_value(o))
            logging.info("record ({}) has changed".format(self.record_id))
        return False

    def notes(self):
        dlg = dialogs.Notes("Treatment notes", self.tx_notes.toPlainText())
        if dlg.exec_() == dlg.Accepted:
            self.tx_notes.clear()
            self.tx_notes.appendPlainText(dlg.tx_plain.toPlainText())
            self.session_mapper.submit()

    def submit_record(self):
        # ...update record
        if not self.record_changed:
            return False
        if not self.session_mapper.submit():
            logging.error("\tError managing session record..." + self.session_model.lastError().text())
            QMessageBox.critical(self, "Update database",
                                 "Error managing session record..." + self.session_model.lastError().text())
            return False
        else:
            logging.info("\tSession (id={}) record stored: OK".format(self.record_id))
        if self.mode == self.NEW_RECORD:
            q = self.session_model.query()
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
            self.session_mapper.toFirst()
        self.act_edit.setChecked(False)
        self.enable_fields(False)
        self.act_edit.setText("Edit")

    def update_form(self, session_key, is_locked):
        self.record_id = session_key
        self.mode = self.SHOW_RECORD
        self.enable_fields(False)
        self.session_model.setFilter("ID={}".format(session_key))
        self.session_model.select()
        row = self.session_model.rowCount()
        if row == 0:
            tx1 = "Database error"
            tx2 = "Wrong ID link between tree and form"
            QMessageBox.critical(self, tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        elif row > 1:
            tx1 = "Database error"
            tx2 = "Two session records with the same ID"
            QMessageBox.critical(self, tx1, tx2)
            logging.error(tx1 + ": " + tx2)
            sys.exit(1)
        self.session_mapper.toFirst()
        self.menu_widget.setVisible(not is_locked)


    def __str__(self):
        s = "#" + str(self.sp_session.value()) + ": " + str(self.tx_isotope.text()) +\
            " (" + str(self.sp_activity.value()) + "MBq @ "
        s += str(self.dt_admin.date().toString("dd/MM/yyyy"))
        s += str(self.dt_admin.time().toString(" HH:mm")) + ")"
        return s