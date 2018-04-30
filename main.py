#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Program ViDi loads an image or a set of DICOM images to do some operations on them.

This class contains most of the gui functionality while the engine of the program is mostly contained in the ImageView
class.

Basic features of ViDi are:
    - Zoom of image(s)
    - Moving through images of the dataset
    - Hybrid modalities registration (shown as watershed overlay)
    - Change WL and watershed levels and opacity
    - ROI drawing and stats extraction
    - Automatic ROI drawing

Other features are expected in the future:
    - internal dosimetry for radionuclide therapy
    - DQE measurement
    - NORMI-13 automatic feature extraction
    - Mammo density definition and dosimetry
    - 3D multiplanar or mpr imaging

Version:
    - 0.1:  Basic features almost done (circular ROI and automatic ROI definition not implemented. ROI stats not shown)
    - 0.2:  BUG of half of pixel displacement @ ViDiGraphics...corrected
            Define a logger on the user's home directory (not complete)
            circular ROI implemented
            Calculates rois statistics and shows a dialog (todo copy roi statistics)
            Separate stats in an object. Implement a Voi object with many rois (i.e. an organ)
            BUG points of moved rois not new_record in scene...corrected
    - 0.3:  ViDi will be DEDICATED ONLY TO INTERNAL DOSIMETRY PURPOSES

BUGS:
    - Changes in font size and line width when zooming
    - Cursor change when hover a pol. roi even if it is not selected
    - Roi stats values are false!!!

IMPROVEMENTS (other minor features to implement or made "on the fly"):
    - Logger to track bugs and errors (not complete)
    - Window and center choices don't like me!!! => Put an histogram in the dialog and some automatic choices.
    - Export image to other formats
    - Copy/paste rois
    - Roi stats dialog
    - Change mouse operations (left button -> Select/rois, wheel-> move between slices/zoom, right ->WL)


"""

import sys
import os
import webbrowser
import logging
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtSql import *
import ui_main
# import ViDiGraphics
import database
from dialogs import *
from mytoolbox import MyToolBox

__author__ = "M.A. Peinado"
__copyright__ = "2018, M.A. Peinado"
__credits__ = ["Miguel A. Peinado"]
__license__ = "GPL"
__version__ = "18.0.1"
__maintainer__ = "M.A. Peinado"
__email__ = "miguel.peinado@sespa.es"
__status__ = "Alpha testing"


class MainGui(QtGui.QMainWindow, ui_main.Ui_MainWindow):

    def __init__(self, screen_width, parent=None):
        # Invoke parent's method
        super(MainGui, self).__init__(parent)
        # <------------------------ Gui setup ----------------------->
        self.setupUi(self)
        # Additional GUI tweaks
        self.showMaximized()
        # <------------------------------ Signals ----------------------------->
        # self.view.view_updated.connect(self.show_message)
        # self.act_show_info.triggered.connect(self.view.show_info)
        # self.tb_edit.actionTriggered.connect(self.set_operation)
        # self.view.roi_finished.connect(self.uncheck_rois)
        # self.act_roi_auto.triggered.connect(self.set_auto_roi)
        # self.act_clone_rois.triggered.connect(self.view.clone_rois)
        # self.act_get_stats.triggered.connect(self.view.show_stats)
        # <----------------------------- Attributes --------------------------->
        self._current_dir = os.getcwd()
        from os.path import expanduser
        self._home_dir = expanduser("~")
        self.show_message("Log file created in " + self._home_dir)
        # ...logger
        logging.basicConfig(format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                            datefmt='%m-%d %H:%M', filename=self._home_dir + '/ViDi.log',
                            filemode='w', level=logging.INFO)
        logging.info('ViDi started')
        self.show()
        #  ...database
        db_path = './database/DataBase.sqlite'
        self.db_connect = QSqlDatabase.addDatabase('QSQLITE')
        self.db_connect.setDatabaseName(db_path)
        if not self.db_connect.open():
            logging.error("Error creating database connection: %s" % self.db_connect.lastError().text())
            QtGui.QMessageBox.critical("Terminate program",
                                       "Error creating database connection: %s" % self.db_connect.lastError().text())
            sys.exit(1)
        else:
            logging.info("Dosimetry database connection opened")

        # Put all these in the right dock
        self.db_widget = database.Tree(db=self.db_connect, parent=self)
        # self.db_widget.empty_tree.connect(self.force_new_patient)
        self.db_widget.pull_message.connect(self.show_message)
        self.dock_widget.setWidget(self.db_widget)
        # self.db_widget.populate()

    def force_new_patient(self):
        def close_dialog():
            logging.critical("EXIT!!!")
            sys.exit(0)
        # dlg = QtGui.QDialog(self)
        dlg = QtGui.QDialog()
        dlg.setWindowTitle("Patients")
        dlg.rejected.connect(close_dialog)
        l = QtGui.QVBoxLayout()
        l.addWidget(QtGui.QLabel("<b>Input patient data...</b>"))
        form = database.PatientForm(self.db_connect, mode=database.PatientForm.NEW_RECORD, parent=self)
        form.new_record_stored.connect(self.buzz)       #dlg.accepted)
        l.addWidget(form)
        l.addWidget(QtGui.QLabel("<b>or...</b>"))
        bt_from_images = QtGui.QPushButton("Get from images")
        bt_from_images.setIcon(QtGui.QIcon(":/image/resources/open-file.svg"))
        # bt_from_images.clicked.connect()
        l.addWidget(bt_from_images)
        dlg.setLayout(l)
        dlg.exec_()
        # update tree
        self.db_widget.populate()


    # def closeEvent(self, ev):
    #     self.fr_dosimetry.about_2_close()
    #     super(MainGui, self).closeEvent(ev)

    # def first_image_loaded(self, image):
    #     self.view.set_image(image[0])      # Unwrap the dicom image
    #
    # def load_overlay_completed(self, overlay_image):
    #     self.view.set_overlay_image(overlay_image[0])   # Unwrap the dicom image
    #
    # def set_operation(self, action):
    #     """Change the operation in the view (See ViDiGraphics)"""
    #     if action == self.act_zoom:
    #         self.view.set_operation(1, self.view.OP_MIDDLE_ZOOM if self.act_zoom.isChecked()
    #                                 else self.view.OP_MIDDLE_CHANGE_Z)
    #     elif action == self.act_roi_pol:
    #         self.view.set_operation(0, self.view.OP_ROI_POL if self.act_roi_pol.isChecked()
    #                                 else self.view.OP_SELECT)
    #         self.act_roi_circ.setChecked(False)
    #         # what if uncheck action when roi not yet finished??
    #     elif action == self.act_roi_circ:
    #         self.view.set_operation(0, self.view.OP_ROI_CIRC if self.act_roi_circ.isChecked()
    #                                 else self.view.OP_SELECT)
    #         self.act_roi_pol.setChecked(False)
    #     elif action == self.act_roi_auto and action.isChecked():
    #         self.view.set_operation(0, self.view.OP_SELECT)
    #         self.act_roi_circ.setChecked(False)
    #         self.act_roi_pol.setChecked(False)
    #
    # def set_auto_roi(self):
    #     draw_auto_roi = self.act_roi_auto.isChecked()
    #     threshold_value = self.spin_threshold.value() if draw_auto_roi else 0
    #     all_images = self.ck_auto_roi_all_images.isChecked() if draw_auto_roi else False
    #     self.view.set_auto_roi(draw_auto_roi, threshold_value, all_images)

    def show_message(self, txt):
        """Show message in status bar"""
        self.status_bar.showMessage(txt)

    # def uncheck_rois(self):
    #     for a in self.tb_edit.actions():
    #         if a != self.act_zoom:
    #             a.setChecked(False)
    #
    # def generate_pdf(self, figure):
    #     text_edit = QTextEdit()
    #     text_edit.setReadOnly(True)
    #     font = text_edit.font()
    #     font.setPointSize(12)
    #     text_edit.setFont(font)
    #     # layout.addWidget(text_edit)
    #     html_text = "<h2><u>Dose report </u><br></h2>"
    #     html_text += "<h3>Patient Data<br></h3>"
    #     html_text += "<p><b>Name: </b>{} (<b>ID: </b>{})".format(self.fr_patient.tx_name.text(),
    #                                                              self.fr_patient.tx_id.text())
    #     age = self.fr_patient.tx_age.text()
    #     age_text = " (" + age + ")" if len(age) > 0 else ""
    #     html_text += "</p><p><b>Birth Date: </b>{} {}<br><br>".format(self.fr_patient.dt_birth_date.text(), age_text)
    #     weight = self.fr_patient.tx_weight.text()
    #     html_text += "</p><p><b>Weight: </b>{}</p></p>".format(weight) if len(weight) > 0 else "</p></p>"
    #     html_text += "<h3>Treatment Data<br></h3>"
    #     html_text += "</p><p><b>Referring Physician: </b>{}</p>".format(self.fr_treatment.tx_physician.text())
    #     html_text += "</p><p><b>Diagnostic: </b>{}</p>".format(self.fr_treatment.tx_diagnostic.text())
    #     html_text += "</p><p><b>Schedule: </b>{}".format(self.fr_treatment.tx_schedule.text())
    #     phm = self.fr_treatment.tx_pharmaceutical.text()
    #     html_text += " (" + phm + ")</p>" if len(phm) > 0 else "</p>"
    #     html_text += "<hr>"
    #     html_text += "</p><p><b>Session number: </b>{}".format(self.fr_session.sp_session.text())
    #     html_text += "</p><p><b>Delivered activity : </b>{} ({})<br><br>".format(self.fr_session.sp_activity.text(),
    #                                                                              self.fr_session.dt_admin.text())
    #     html_text += "<h3>Organ Doses<br></h3>"
    #     html_text += "<p><b>Method: </b>MIRD S-voxel</p>"
    #     html_text += "<table border=0 cellspacing=0 cellpadding=2>"
    #     html_text += "<tr><td> <b>Quantification factor: </b> {} (MBq/count)        </td>" \
    #                  "<td> <b>(&Delta;f/f)<sup>2</sup>: </b> {}</td></tr>".format(self.fr_dosimetry.tx_f_quant.text(),
    #                                                                         self.fr_dosimetry.tx_delta_f.text())
    #     html_text += "<tr><td> <b>S<sub>ref</sub>: </b> {} (count/MBq)</td>" \
    #                  "<td> <b>S<sub>actual</sub>: </b> {} (count/MBq)</td>" \
    #                  "</tr></table>".format(self.fr_dosimetry.tx_s_ref.text(),
    #                                         self.fr_acquisition.tx_sensitivity.text())
    #     text_edit.append(html_text)
    #     # ...add image (from stackoverflow.com questions/15539075/inserting-qimage-after-string-in-qtextedit)
    #     figure.seek(0)
    #     buf = QByteArray(figure.read())
    #     pixmap = QPixmap()
    #     pixmap.loadFromData(buf, format="PNG")
    #     text_cursor = text_edit.textCursor()
    #     text_cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
    #     im = pixmap.toImage()
    #     # ...scale image to fit in a page (15 cm width)
    #     text_cursor.insertImage(im.scaledToWidth(0.15 * im.dotsPerMeterX(), Qt.SmoothTransformation))
    #     vois = self.view.scene().voi_box.get_vois()
    #     html_text = "<table border=1 cellspacing=0 cellpadding=2>"
    #     # ...headers
    #     html_text += "<thead><tr bgcolor=#f0f0f0>"
    #     html_text += "<th>Organ</th><th>&tau; (hours)</th><th>(&Delta;&tau;/&tau;)<sup>2</sup></th>" \
    #                  "<th>Av. Dose (mGy)</th><th>&Delta;D (mGy)</th></tr></thead>"
    #     for v in vois:
    #         html_text += "<tr><td align='center'>{}</td>".format(v.label)
    #         html_text += "<td align='center'>{:.4g}</td>".format(v.residence_time / 3600.)
    #         html_text += "<td align='center'>{:.4g}</td>".format(v.delta_tau_sq)
    #         html_text += "<td align='center'>{:.4g}</td>".format(v.average_dose)
    #         html_text += "<td align='center'>{:.4g}</td></tr>".format(v.delta_d)
    #     html_text += "</table><br><br><br><br><br><br>"
    #     html_text += "<p style=text-align:right> {} </p>".format(self.fr_dosimetry.tx_physicist.text())
    #     text_edit.append(html_text)
    #     printer = QPrinter(QPrinter.HighResolution)
    #     printer.setOutputFormat(QPrinter.PdfFormat)
    #     printer.setOutputFileName("dose_report.pdf")
    #     printer.setColorMode(QPrinter.Color)
    #     text_edit.document().print_(printer)
    #     txt = "Report created in {}/dose_report.pdf".format(self._current_dir)
    #     QtGui.QMessageBox.information(self, "ViDi: Dosimetry", txt)
    #     logging.info(txt)
    #     webbrowser.open_new(r"dose_report.pdf")

# Autolauncher
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet("QToolButton::disabled{border-style: solid; border-width: 1px; border-color: rgb(170, 170, 170);"
                      " border-top-right-radius: 10px; border-bottom-left-radius: 10px;"
                      " border-bottom-right-radius: 10px; padding: 3px; margin: 2px;}"
                      "QToolButton::enabled{border-style: solid; border-width: 1px;"
                      " border-color: rgb(170, 170, 170); border-top-right-radius: 10px;"
                      " border-bottom-left-radius: 10px; background-color: qlineargradient(spread:pad,"
                      " x1:0, y1:0, x2:0, y2:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));"
                      " border-bottom-right-radius: 10px; padding: 3px; margin: 2px;}"
                      "QToolButton::hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
                      " stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));}"
                      "QToolButton::pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
                      " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
                      "QToolButton::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
                      " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
                      "QPushButton::disabled{border-style: solid; border-width: 1px; border-color: rgb(170, 170, 170);"
                      " border-top-right-radius: 10px; border-bottom-left-radius: 10px;"
                      " border-bottom-right-radius: 10px; padding: 3px; margin: 2px;}"
                      "QPushButton::enabled{border-style: solid; border-width: 1px;"
                      " border-color: rgb(170, 170, 170); border-top-right-radius: 10px;"
                      " border-bottom-left-radius: 10px; background-color: qlineargradient(spread:pad,"
                      " x1:0, y1:0, x2:0, y2:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));"
                      " border-bottom-right-radius: 10px; padding: 3px; margin: 2px;}"
                      "QPushButton::hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
                      " stop:0 rgba(255, 255, 255, 255), stop:1 rgba(192, 255, 192, 255));}"
                      "QPushButton::pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
                      " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
                      "QPushButton::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,"
                      " stop:0 rgba(128, 170, 128, 255), stop:1 rgba(192, 255, 192, 255));}"
                      )
    screen_w = app.desktop().screenGeometry().width()
    c = MainGui(screen_w)
    app.exec_()
