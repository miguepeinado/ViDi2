# -*- coding: utf-8 -*-
import sys
import logging
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtSql
import icons_rc
import patient, treatment, session, dosimetry


class Tree(QtGui.QFrame):

    pull_message = QtCore.pyqtSignal(QtCore.QString)
    # node_selected = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    #
    # How to lock all children of a locked node?
    # 1. In DB best but too many work
    # 2. In tree: Easy but means inconsistencied between DB and GUI
    #

    def __init__(self, db, parent=None):
        # Invoke parent's method
        super(Tree, self).__init__(parent)
        # init some variables
        self.db = db
        self.levels = ["P", "T", "S", "D", "A", "I"]
        # Setup gui...
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        l = QtGui.QVBoxLayout()
        self.db_tree = QtGui.QTreeView(self)
        self.db_tree.setMinimumHeight(450)
        self.db_tree.setIndentation(16)
        self.db_tree.setIconSize(QtCore.QSize(20, 20))
        self.db_tree.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        self.db_tree.clicked.connect(self.item_clicked)

        # ...context menu
        self.context_menu = QtGui.QMenu()
        self.act_new_patient = QtGui.QAction(QtGui.QIcon(":/database/resources/new-patient.svg"),
                                         "New patient", self.context_menu)
        self.act_new_patient.triggered.connect(self.new_patient)
        self.context_menu.addAction(self.act_new_patient)
        self.act_new_treatment = QtGui.QAction(QtGui.QIcon(":/database/resources/treatment.svg"),
                                               "New treatment", self.context_menu)
        self.act_new_treatment.triggered.connect(self.new_treatment)
        self.context_menu.addAction(self.act_new_treatment)
        self.act_new_session = QtGui.QAction(QtGui.QIcon(":/database/resources/medicine.svg"),
                                               "New session", self.context_menu)
        self.act_new_session.triggered.connect(self.new_session)
        self.context_menu.addAction(self.act_new_session)
        self.act_new_dosimetry = QtGui.QAction(QtGui.QIcon(":/database/resources/trebol.svg"),
                                             "New dosimetry", self.context_menu)
        self.act_new_dosimetry.triggered.connect(self.new_dosimetry)
        self.context_menu.addAction(self.act_new_dosimetry)
        self.act_new_assay = QtGui.QAction(QtGui.QIcon(":/database/resources/experimental.svg"),
                                               "New assay", self.context_menu)
        self.act_new_assay.triggered.connect(self.new_assay)
        self.context_menu.addAction(self.act_new_assay)
        self.act_new_image = QtGui.QAction(QtGui.QIcon(":/database/resources/image1.svg"),
                                               "New image dataset", self.context_menu)
        self.act_new_image.triggered.connect(self.new_image)
        self.context_menu.addAction(self.act_new_image)
        self.db_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.db_tree.customContextMenuRequested.connect(self.open_context_menu)

        # Widgets...
        l.addWidget(self.db_tree)
        self.space_keeper = QtGui.QLabel(" ")
        self.space_keeper.setFixedSize(QtCore.QSize(400, 200))
        l.addWidget(self.space_keeper)
        # ...Patient form
        self.patient_form = patient.PatientForm(self.db)
        self.patient_form.record_updated.connect(self.update_item)
        self.patient_form.setFixedWidth(400)
        l.addWidget(self.patient_form)
        self.patient_form.setVisible(False)
        # ...Treatment form
        self.treatment_form = treatment.TreatmentForm(self.db)
        self.treatment_form.record_updated.connect(self.update_item)
        self.treatment_form.lock_record.connect(self.lock_item)
        self.treatment_form.setFixedWidth(400)
        l.addWidget(self.treatment_form)
        self.treatment_form.setVisible(False)
        # ...Session form
        self.session_form = session.SessionForm(self.db)
        self.session_form.record_updated.connect(self.update_item)
        self.session_form.lock_record.connect(self.lock_item)
        self.session_form.setFixedWidth(400)
        l.addWidget(self.session_form)
        self.session_form.setVisible(False)
        # ...Session form
        self.dosimetry_form = dosimetry.DosimetryForm(self.db)
        self.dosimetry_form.record_updated.connect(self.update_item)
        self.dosimetry_form.lock_record.connect(self.lock_item)
        self.dosimetry_form.setFixedWidth(400)
        l.addWidget(self.dosimetry_form)
        self.dosimetry_form.setVisible(False)
        spring = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        l.addItem(spring)
        self.setLayout(l)
        # Populate tree
        self.tree_model = MyModel(self.db, parent=self)
        self.db_tree.setModel(self.tree_model)
        self.tree_model.populate()

    def item_clicked(self, ix):
        item_type, item_key = self.tree_model.itemFromIndex(ix).get_key()
        locked = self.tree_model.itemFromIndex(ix).is_locked()
        self.space_keeper.setVisible(False)
        # Hide all the frames
        for c in self.children():
            if isinstance(c, QtGui.QFrame) and not type(c) == QtGui.QTreeView:
                c.setVisible(False)
        # Show only de correct one
        if item_type == "P":
            self.patient_form.setVisible(True)
            self.patient_form.update_form(item_key)
        elif item_type == "T":
            self.treatment_form.setVisible(True)
            self.treatment_form.update_form(item_key, locked)
        elif item_type == "S":
            self.session_form.setVisible(True)
            self.session_form.update_form(item_key, locked)
        elif item_type == "D":
            self.dosimetry_form.setVisible(True)
            self.dosimetry_form.update_form(item_key, locked)
        else:
            self.space_keeper.setVisible(True)

    def new_assay(self):
        pass

    def new_dosimetry(self):
        # get parent node
        ix = self.db_tree.currentIndex()
        parent_item = self.tree_model.itemFromIndex(ix)
        item_type, key = parent_item.get_key()
        if item_type == "D":
            parent_item = parent_item.parent()
            _, key = parent_item.get_key()
        # if item type is "S" selected node is the parent node actually
        # Count number of sessions present
        dlg = QtGui.QDialog()
        dlg.setWindowTitle("New Dosimetry")
        l = QtGui.QVBoxLayout()
        sn = parent_item.rowCount() + 1
        form = dosimetry.DosimetryForm(self.db, mode=dosimetry.DosimetryForm.NEW_RECORD,
                                       parent_id=key, parent=self)
        form.new_record_stored.connect(dlg.accept)
        l.addWidget(form)
        dlg.setLayout(l)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            # Add new row instead of repopulate all the tree
            tx_key = "D#" + str(form.record_id)
            txt = str(form)
            item = MyItem(txt, tx_key, QtGui.QIcon(":/database/resources/trebol.svg"),
                          locked=False, is_header=False)
            parent_item.appendRow(item)
            dlg.close()

    def new_image(self):
        pass

    def new_patient(self, force_input):
        """
        :param force_input: Force input of a new patient or exit program (when tree is empty)
        :return: nothing
        """

        dlg = QtGui.QDialog()
        dlg.setWindowTitle("New Patient")
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
            txt = str(form)
            item = MyItem(txt, tx_key, QtGui.QIcon(":/database/resources/new-patient.svg"),
                          locked=False, is_header=True)
            self.tree_model.appendRow(item)
            dlg.close()
        else:
            if force_input:
                QtGui.QMessageBox.critical(self, "Update database", "Input patient failed. Must exit")
                sys.exit(1)

    def new_treatment(self):
        # get parent node
        ix = self.db_tree.currentIndex()
        # todo: Verify what happens when new treatment is triggered from patient node
        parent_item = self.tree_model.itemFromIndex(ix).parent()
        if parent_item is None:
            parent_item = self.tree_model.itemFromIndex(ix)
        _, key = parent_item.get_key()
        dlg = QtGui.QDialog()
        dlg.setWindowTitle("New Treatment")
        l = QtGui.QVBoxLayout()
        form = treatment.TreatmentForm(self.db, mode=treatment.TreatmentForm.NEW_RECORD,
                                       parent_id=key, parent=self)
        form.new_record_stored.connect(dlg.accept)
        l.addWidget(form)
        dlg.setLayout(l)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            # Add new row instead of repopulate all the tree
            tx_key = "T#" + str(form.record_id)
            txt = str(form)
            item = MyItem(txt, tx_key, QtGui.QIcon(":/database/resources/treatment.svg"),
                          locked=False, is_header=False)
            parent_item.appendRow(item)
            dlg.close()

    def new_session(self):
        # get parent node
        ix = self.db_tree.currentIndex()
        parent_item = self.tree_model.itemFromIndex(ix)
        item_type, key = parent_item.get_key()
        if item_type == "S":
            parent_item = parent_item.parent()
            _, key = parent_item.get_key()
        # if item type is "T" selected node is the parent node actually
        # Count number of sessions present
        dlg = QtGui.QDialog()
        dlg.setWindowTitle("New Session")
        l = QtGui.QVBoxLayout()
        sn = parent_item.rowCount() + 1
        form = session.SessionForm(self.db, mode=session.SessionForm.NEW_RECORD,
                                   parent_id=key, session_number=sn, parent=self)
        form.new_record_stored.connect(dlg.accept)
        l.addWidget(form)
        dlg.setLayout(l)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            # Add new row instead of repopulate all the tree
            tx_key = "S#" + str(form.record_id)
            txt = str(form)
            item = MyItem(txt, tx_key, QtGui.QIcon(":/database/resources/medicine.svg"),
                          locked=False, is_header=False)
            parent_item.appendRow(item)
            dlg.close()

    def open_context_menu(self, position):
        ix = self.db_tree.indexAt(position)
        item = self.tree_model.itemFromIndex(ix)
        node_is_locked = item.is_locked()
        t, _ = item.get_key()
        level = self.levels.index(t)
        # Hide or disable action following node level
        # Does it work for level>3?
        menu_action_list = self.context_menu.actions()
        for a in menu_action_list:
            ix = menu_action_list.index(a)
            is_visible = (level < 3 and 0 <= (ix - level) <= 1) or (2 < level <= ix)
            a.setVisible(is_visible)
            is_enabled = (level == ix or not node_is_locked)
            a.setEnabled(is_enabled)
        self.context_menu.exec_(self.db_tree.viewport().mapToGlobal(position))

    def update_item(self, txt):
        ix = self.db_tree.currentIndex()
        item = self.tree_model.itemFromIndex(ix)
        item.setText(txt)

    def lock_item(self):
        ix = self.db_tree.currentIndex()
        item = self.tree_model.itemFromIndex(ix)
        item.set_locked(True)
        self.db_tree.update(ix)


class MyModel(QtGui.QStandardItemModel):
    """
    Model for dosimetry tree
    """
    tables = ["Patients", "Treatments", "Sessions", "Dosimetries", "Acquisitions"]

    def __init__(self, db, parent=None):
        super(MyModel, self).__init__(0, 1,  parent)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Dosimetry Database")
        self.db = db
        self.level = 0
        # icons
        self.node_icons = [QtGui.QIcon(":/database/resources/patient.svg"),
                           QtGui.QIcon(":/database/resources/treatment.svg"),
                           QtGui.QIcon(":/database/resources/medicine.svg"),
                           QtGui.QIcon(":/database/resources/trebol.svg"),
                           QtGui.QIcon(":/database/resources/experimental.svg"),
                           QtGui.QIcon(":/database/resources/image1.svg")]

    def populate(self, parent_node=None, level=0):
        # Stopper for the recursive items filling from different tables
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
        elif level == 3:
            tx_query += " WHERE N_Session={}".format(value)
        elif level > 3:
            tx_query += " WHERE N_Dosimetry={}".format(value)
        logging.info("Executing query '{}' for ".format(tx_query))
        query.exec_(tx_query)
        query.first()
        if not query.isValid():
            if level == 0:
                logging.info("no patients in database...must input one")
                self.parent().new_patient(force_input=True)
            return
        while True:
            header = False
            locked = False
            highlighted = False
            tx_key = self.tables[level][0]
            icon = self.node_icons[level]
            if level == 0:
                header = True
                txt = query.value(1).toString() + " (" + query.value(0).toString() + ")"
            elif level == 1:
                locked = query.value(8).toBool()
                txt = query.value(2).toString()
                txt += " (" + query.value(3).toString() + ")" if not query.value(3).isNull() else ""
                print txt + "<<< treatment locked >>>" if locked else ""
            elif level == 2:
                locked = query.value(6).toBool()
                txt = "#" + query.value(2).toString() + ": " + query.value(4).toString() + \
                      " (" + query.value(3).toString() + "MBq @ "
                txt += query.value(5).toDate().toString("dd/MM/yyyy")
                txt += query.value(5).toTime().toString(" HH:mm") + ")"
            elif level == 3:
                highlighted = query.value(4).toBool()
                txt = "Dosimetry: " + query.value(2).toDate().toString("dd/MM/yyyy")
                txt += ". Approved by " + str(query.value(3).toString()) if query.value(5).toBool() else ""
            elif level > 3:
                txt = query.value(3).toString() + query.value(2).toDate().toString("dd/MM/yyyy")
                if query.value(4).toString() != "ASSAY":
                    tx_key = "I"
                    icon = self.node_icons[level + 1]
            key = query.value(0)
            k, _ = key.toInt()
            key = key.toString() if level == 0 else k
            tx_key += "#" + str(key)
            print "item: key={}, text={}".format(tx_key, txt)
            item = MyItem(txt, tx_key, icon, locked, highlighted, is_header=header)
            # Stopper for the recursive items filling from different tables
            if level < 4:
                self.populate(item, level + 1)
            parent_node.appendRow(item)
            if not query.next():
                break


class MyItem(QtGui.QStandardItem):
    """
    Subclassing tree items
    - key: Allows a link between parent and children nodes
    - locked: Let know if node is always locked
    - is_header:
    """

    def __init__(self, text, key="", icon=None, locked=True, highlighted=False, is_header=False):
        if icon is not None:
            super(MyItem, self).__init__(icon, text)
        else:
            super(MyItem, self).__init__(text)
        self.highlighted = highlighted
        self.is_header = is_header
        self.key = key
        self.locked = locked
        # Change colors after its role
        fnt = self.font()
        if locked:
            fnt.setItalic(True)
            self.setForeground(QtGui.QBrush(QtGui.QColor(0, 192, 0)))
            self.setBackground(QtGui.QBrush(QtGui.QColor(224, 224, 224)))
            self.setToolTip("Inactive record")
        elif self.highlighted:
            self.setForeground(QtGui.QBrush(QtGui.QColor(0, 192, 0)))
            self.setBackground(QtGui.QBrush(QtGui.QColor(255, 186, 159)))
            self.setToolTip("Highlighted record")
        if self.is_header:
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

    def is_locked(self):
        return self.locked

    def set_locked(self, locked):
        self.locked = locked
        fnt = self.font()
        fnt.setItalic(locked)
        if locked:
            self.setForeground(QtGui.QBrush(QtGui.QColor(0, 192, 0)))
            self.setBackground(QtGui.QBrush(QtGui.QColor(224, 224, 224)))
            self.setToolTip("Inactive record")
        else:
            self.setForeground(QtGui.QBrush(QtCore.Qt.black))
            self.setBackground(QtGui.QBrush(QtCore.Qt.white))

    def set_highlighted(self, highlighted):
        if not self.locked:
            return
        self.highlighted = highlighted
        fore_color = QtGui.QColor(0, 192, 0) if self.highlighted else QtGui.QColor(0, 127, 0)
        self.setForeground(QtGui.QBrush(fore_color))
        back_color = QtGui.QColor(255, 186, 159) if self.highlighted else QtGui.QColor(255, 255, 255)
        self.setBackground(QtGui.QBrush(back_color))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    t = Tree("")
    t.show()
    app.exec_()
    sys.exit(0)