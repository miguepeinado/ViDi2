from PyQt4 import QtCore
from PyQt4 import QtGui
import ui_notes


class Notes(QtGui.QDialog, ui_notes.Ui_Dialog):

    def __init__(self, title="", txt="", parent=None):
        super(Notes, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.tx_plain.appendPlainText(txt)
        self.setLayout(self.grid_layout)
        self.resize(500, 200)
        # Signals/slots
        self.bt_clear_text.clicked.connect(self.tx_plain.clear)