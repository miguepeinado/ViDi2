# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyToolBox(QScrollArea):

    def __init__(self, parent=None):
        super(MyToolBox, self).__init__(parent)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        contents_widget = QFrame(self)
        contents_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setWidget(contents_widget)
        self.contents_layout = QVBoxLayout()
        self.contents_layout.setSpacing(0)
        contents_widget.setLayout(self.contents_layout)
        self.contents_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setMinimumWidth(400)

    def add_item(self, widget, text, visible=True):
        i = MyItem(widget, text, visible, self)
        i.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        pos = self.contents_layout.count() - 1
        self.contents_layout.insertWidget(pos, i)


class MyItem(QFrame):

    def __init__(self, widget, text, visible, parent):
        super(MyItem, self).__init__(parent)
        # todo make icons line thinner
        self.collapsed_icon = QIcon(":Actions/pictures/item-collapsed.svg")
        self.expanded_icon = QIcon(":Actions/pictures/item-expanded.svg")
        self.widget = widget
        self.widget_visible = visible
        self.default_text = text
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.button = QPushButton("")
        self.button.setText(self.get_text())
        self.button.setStyleSheet("Text-align: left")
        self.button.setCheckable(True)
        self.button.setChecked(visible)
        icon = self.expanded_icon if self.button.isChecked() else self.collapsed_icon
        self.button.setIcon(icon)
        self.button.clicked.connect(self.change_visible)
        layout.addWidget(self.button)
        layout.addWidget(self.widget)
        self.widget.setVisible(self.widget_visible)

    def change_visible(self):
        self.widget_visible = not self.widget_visible
        icon = self.expanded_icon if self.widget_visible else self.collapsed_icon
        self.button.setText(self.get_text())
        self.button.setIcon(icon)
        self.widget.setVisible(self.widget_visible)
    
    def get_text(self):
        s = str(self.default_text)
        s += (": " + str(self.widget)) if not self.widget_visible else ""
        fm = self.button.fontMetrics()
        s = fm.elidedText(s, Qt.ElideRight, 320)
        return s