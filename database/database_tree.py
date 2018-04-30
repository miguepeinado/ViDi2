# -*- coding: utf-8 -*-
import sys
import logging
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtSql
import icons_rc
import patient


class Tree(QtGui.QFrame):

    pull_message = QtCore.pyqtSignal(QtCore.QString)
    node_selected = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)

    def __init__(self, db, parent=None):
        # Invoke parent's method
        super(Tree, self).__init__(parent)
        self.db = db
        # Setup gui
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        l = QtGui.QVBoxLayout()
        self.db_tree = QtGui.QTreeView(self)
        self.db_tree.setMinimumHeight(250)
        self.db_tree.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        self.db_tree.clicked.connect(self.item_clicked)
        # ...context menu
        self.context_menu = QtGui.QMenu()
        self.act_new_patient = QtGui.QAction(QtGui.QIcon(":/database/resources/new-patient.svg"),
                                         "New patient", self.context_menu)
        self.act_new_patient.triggered.connect(self.new_patient)
        self.context_menu.addAction(self.act_new_patient)
        self.db_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.db_tree.customContextMenuRequested.connect(self.open_context_menu)
        l.addWidget(self.db_tree)
        self.spacer = QtGui.QLabel(" ")
        self.spacer.setFixedSize(QtCore.QSize(400, 200))
        l.addWidget(self.spacer)
        self.patient_form = patient.PatientForm(self.db)
        self.spacer.setFixedSize(QtCore.QSize(400, 200))
        l.addWidget(self.patient_form)
        self.patient_form.setVisible(False)
        self.setLayout(l)
        # Populate tree
        self.tree_model = MyModel(self.db, parent=self)
        self.db_tree.setModel(self.tree_model)
        self.tree_model.populate()

    def item_clicked(self, ix):
        item_type, item_key = self.tree_model.itemFromIndex(ix).get_key()
        self.spacer.setVisible(False)
        if item_type == "P":
            self.patient_form.setVisible(True)
            self.patient_form.update_form(item_key)
        elif item_type == "T":
            self.patient_form.setVisible(False)
            self.spacer.setVisible(True)
        elif item_type == "S":
            self.patient_form.setVisible(False)
            self.spacer.setVisible(True)

    def new_patient(self, force_input):
        """
        :param force_input: Force input of a new patient or exit program (when tree is empty)
        :return: nothing
        """

        dlg = QtGui.QDialog()
        dlg.setWindowTitle("Patients")
        l = QtGui.QVBoxLayout()
        l.addWidget(QtGui.QLabel("<b>First of all, please input patient data...</b>"))
        form = patient.PatientForm(self.db, mode=patient.PatientForm.NEW_RECORD, parent=self)
        form.new_record_stored.connect(dlg.accept)
        l.addWidget(form)
        l.addWidget(QtGui.QLabel("<b>or...</b>"))
        bt_from_images = QtGui.QPushButton("Gather patient data from images")
        bt_from_images.setIcon(QtGui.QIcon(":/image/resources/open-file.svg"))
        l.addWidget(bt_from_images)
        dlg.setLayout(l)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            # Add new row instead of repopulate all the tree
            tx_key = "P#" + str(form.tx_id.text())
            txt = str(form.tx_name.text())
            item = MyItem(txt, tx_key, QtGui.QIcon(":/database/resources/new-patient.svg"),
                          active=True, is_header=False)
            self.tree_model.appendRow(item)
            dlg.close()
        else:
            if force_input:
                QtGui.QMessageBox.critical(self, "Update database", "Input patient failed. Must exit")
                sys.exit(1)

    def open_context_menu(self, position):
        self.context_menu.exec_(self.db_tree.viewport().mapToGlobal(position))

    # def populate(self):
    #     self.tree_model.populate()


class MyModel(QtGui.QStandardItemModel):
    """
    Model for dosimetry tree
    """
    tables = {0: "Patients", 1: "Treatments", 2: "Sessions"}

    def __init__(self, db, parent=None):
        super(MyModel, self).__init__(0, 1,  parent)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Dosimetry Database")
        self.db = db
        self.level = 0
        # icons
        self.node_icons = [QtGui.QIcon(":/database/resources/patient.svg"),
                           QtGui.QIcon(":/database/resources/treatment.svg"),
                           QtGui.QIcon(":/database/resources/medicine.svg")]

    def populate(self, parent_node=None, level=0):
        # Stopper for the recursive items filling from different tables
        if level > 2:
            return
        query = QtSql.QSqlQuery(self.db)
        try:
            _, value = parent_node.get_key()
        except AttributeError:
            value = None
            parent_node = self
        tx_query = "SELECT * FROM " + self.tables[level]
        if level == 1:
            tx_query += " WHERE N_Patient='{}'".format(value)
        elif level == 2:
            tx_query += " WHERE N_Treatment={}".format(value)
        logging.info("Executing query '{}' for ".format(tx_query))
        query.exec_(tx_query)
        query.first()
        if not query.isValid():
            if level == 0:
                logging.info("no patients in database...must input one")
                self.parent().new_patient(force_input=True)
            return
        while True:
            active = True
            if level == 0:
                txt = query.value(1).toString() + " (" + query.value(0).toString() + ")"
            elif level == 1:
                txt = query.value(2).toString()
                txt += " (" + query.value(3).toString() + ")" if not query.value(3).isNull() else ""
            elif level == 2:
                txt = query.value(4).toString()
                txt += " (" + query.value(3).toString() + " MBq)"
            key = query.value(0)
            k, _ = key.toInt()
            key = key.toString() if level == 0 else k
            tx_key = self.tables[level][0] + "#" + str(key)
            print "item: key={}, text={}".format(tx_key, txt)
            item = MyItem(txt, tx_key, self.node_icons[level], active, is_header=False)
            self.populate(item, level + 1)
            parent_node.appendRow(item)
            if not query.next():
                break


class MyItem(QtGui.QStandardItem):
    """
    Subclassing tree items
    - key: Allows a link between parent and children nodes
    - active: Let know if node is always active
    - is_header:
    """

    def __init__(self, text, key="", icon=None, active=True, highlighted=False, is_header=False):
        if icon is not None:
            super(MyItem, self).__init__(icon, text)
        else:
            super(MyItem, self).__init__(text)
        self.highlighted = highlighted
        self.is_header = is_header
        self.key = key
        self.active = active
        # Segun su rol cambiamos el aspecto
        fnt = self.font()
        fnt.setPointSize(10)
        if not active:
            self.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.setBackground(QtGui.QBrush(QtGui.QColor(255, 32, 32)))
            self.setToolTip("Inactive record")
        elif self.highlighted:
            self.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.setBackground(QtGui.QBrush(QtGui.QColor(255, 186, 159)))
            self.setToolTip("Highlighted record")
        if self.is_header:
            fnt.setPointSize(11)
            fnt.setWeight(50)
            fnt.setStretch(125)
        self.setFont(fnt)
        # Lo hacemos no editable
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsEditable)

    def get_key(self):
        i = self.key.find('#')
        item_type = self.key[:i]
        key_value = self.key[i + 1:]
        return item_type, key_value

    def is_active(self):
        return self.active

    def set_highlighted(self, highlighted):
        if not self.active:
            return
        self.highlighted = highlighted
        fore_color = QtGui.QColor(255, 255, 255) if self.highlighted else QtGui.QColor(0, 127, 0)
        self.setForeground(QtGui.QBrush(fore_color))
        back_color = QtGui.QColor(255, 186, 159) if self.highlighted else QtGui.QColor(255, 255, 255)
        self.setBackground(QtGui.QBrush(back_color))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    t = Tree("")
    t.show()
    app.exec_()
    sys.exit(0)