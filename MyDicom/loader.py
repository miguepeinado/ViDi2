#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from os.path import expanduser
import numpy as np
import PyQt4.QtCore
import PyQt4.QtGui
import dicom
from dicom_image import DicomImage
from patient_data import PatientData
import tools

__author__ = "M.A. Peinado"
__copyright__ = "2016, M.A. Peinado"
__credits__ = ["Miguel A. Peinado"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "M.A. Peinado"
__email__ = "miguel.peinado@sespa.es"
__status__ = "prototype"


class ImageLoader(PyQt4.QtCore.QThread):
    """
        This QThread subclass is responsible for loading CORRECTLY all the images. in background
        and show the first one
    """
    first_loaded = PyQt4.QtCore.pyqtSignal(list)   # wrap DicomImage in list
    # updated = PyQt4.QtCore.pyqtSignal(int)
    updated = PyQt4.QtCore.pyqtSignal(basestring)
    completed = PyQt4.QtCore.pyqtSignal(list)   # wrap DicomImage in list

    def __init__(self, files2open, is_overlay=False):
        super(ImageLoader, self).__init__()
        self.files2open = files2open
        self.is_overlay = is_overlay
        self.is_sequence = False            # Can be local????

    def run(self):
        z_positions = []
        n_images = len(self.files2open)
        dicom_image = DicomImage()
        self.is_sequence = n_images > 1
        # call dicom to open the file
        i = 0
        path_sep = os.sep
        home_path = expanduser("~")
        for f in self.files2open:
            file_name = f
            file_name = file_name.replace(home_path, "~")
            n = len(file_name.split(path_sep))
            if n > 2:
                pos1 = file_name.find(path_sep) + len(path_sep)
                pos2 = file_name.rfind(path_sep)
                file_name = file_name[:pos1] + "..." + file_name[pos2:]
            message_text = "loading %i/%i: %s" % (i+1, n_images, file_name)
            logging.info(message_text)
            dicom_file = dicom.read_file(f)
            stored_values = dicom_file.pixel_array
            # 3D dataset can't be included in a list of images
            if len(stored_values.shape) > 2 and self.is_sequence:
                    raise IndexError("the file already contains a 3D array")
            # Get general data: dimensions, bits arrangement
            rows = dicom_file.Rows
            cols = dicom_file.Columns
#
# Pixel arrangement
#
            allocated = dicom_file.BitsAllocated
            stored = dicom_file.BitsStored
            high_bit = dicom_file.HighBit
            if high_bit >= stored:
                reduction_factor = 2.**(high_bit + 1 - stored)
                print "reduction factor of stored values: ", reduction_factor
                stored_values /= reduction_factor
#
# Color images
#
            samples_per_pixel = dicom_file.SamplesPerPixel
            if samples_per_pixel > 1:
                # todo: accept color images
                print "can`t deal with color images...throws an exception"
#
# Unsigned or signed (two complement is dicom mandatory)
#
            signed = (dicom_file.PixelRepresentation != 0)
            inverted = (dicom_file.PhotometricInterpretation == 'MONOCHROME1')
#
# Get the values for (screen) pixel values
#
            w = long(np.max(stored_values)) - long(np.min(stored_values))
            window = dicom_file.WindowWidth if ('WindowWidth' in dicom_file) else w
            center = dicom_file.WindowCenter if ('WindowCenter' in dicom_file) else w/2

            # ...Pixel array type
            data_type = stored_values.dtype
            # pack all the values and emit the signal to the main window
            # np.savetxt("stored values.csv", stored_values, delimiter=",")

# Transform to float for easier manipulation
            stored_values = stored_values.astype(float)
#
# 1st of all, padding if necessary...
#
            padding_value = dicom_file.PixelPaddingValue if ('PixelPaddingValue' in dicom_file) else None
            if padding_value is not None:
                if 'PixelPaddingRangeLimit' in dicom_file:
                    padding_range_limit = dicom_file.PixelPaddingRangeLimit
                else:
                    padding_range_limit = None
                # ...Verify PadVal is bigger than maximum possible value
                if signed:
                    padding_value = self.complement2(padding_value, stored)
                    if padding_range_limit is not None:
                        padding_range_limit = self.complement2(padding_range_limit, stored)
                # apply padding values to the stores values array
                if inverted:
                    if padding_range_limit is not None:
                        pass
                    else:
                        stored_values[stored_values >= padding_value] = np.NaN
                else:
                    if padding_range_limit is not None:
                        pass
                    else:
                        stored_values[stored_values <= padding_value]=np.NaN
#
# Transform to output units
#
            intercept = float(dicom_file.RescaleIntercept) if ('RescaleIntercept' in dicom_file) else None
            pixel_units = None
            if intercept is not None:
                # Lazily verification: slope must exist if intercept is not None
                slope = float(dicom_file.RescaleSlope)
                pixel_units = dicom_file.RescaleType if ('RescaleType' in dicom_file) else 'NO'
                # print "rescale type: ", pixel_units
                ou = stored_values*slope
                ou += intercept
            else:
                # todo: Must process also modality lut
                ou = np.copy(stored_values)
            # np.savetxt("output units.csv", ou, delimiter=",")
            # First time make some operations
            if i == 0:
                if not self.is_sequence and len(ou.shape) > 2:       # 3D dataset in a single file
                    self.is_sequence = True
                    n_images = ou.shape[0]
                    output_units = np.copy(ou)
                    # dicom_image.set_slice_locations()
                else:                           # 2D images
                    output_units = ou[np.newaxis, :, :]
                # todo: Arrange for 2D image sequences without no spatial information (try/catch sentences)
                element , _ = tools.in_(dicom_file, 'FrameOfReferenceUID')
                cfr_uid = element.value
                element, _ = tools.in_(dicom_file, 'ImageOrientationPatient')
                cs_xy = [float(x) for x in element.value]       # Transform to float values
                element, _ = tools.in_(dicom_file, 'ImagePositionPatient')
                im_pos = [float(x) for x in element.value]      # Transform to float values
                element, _ = tools.in_(dicom_file, 'PixelSpacing')
                px_spacing = [float(x) for x in element.value]  # Transform to float values
                slice_thickness = dicom_file.SliceThickness if 'SliceThickness' in dicom_file else None
                # Loads demographic data
                patient_data = PatientData(dicom_file)
                date, time = self.get_date_time_acquisition(dicom_file)
                self.general_attributes = {'allocated': allocated, 'stored': stored, 'high_bit': high_bit,
                                           'samples_per_pixel': samples_per_pixel,
                                           'rows': rows, 'cols': cols, 'n_images': n_images,
                                           'window': window, 'center': center, 'data_type': data_type,
                                           'pixel_units': pixel_units, 'padVal': padding_value, 'inverted': inverted,
                                           'frame_uid': cfr_uid, 'cosines':cs_xy, 'slice_thickness': slice_thickness,
                                           'origin': im_pos, 'pixel_spacing': px_spacing, 'patient_data': patient_data,
                                           'acq_date_time': (date, time)}
                dicom_image.set_attributes(self.general_attributes)
                dicom_image.is_sequence = self.is_sequence
                dicom_image.is_overlay = self.is_overlay
                dicom_image.set_default_color_table()
                dicom_image.set_pixel_values(output_units)
                self.first_loaded.emit([dicom_image])
            else:
                # verify attributes with the rest of the files
                if rows != self.general_attributes['rows'] or cols != self.general_attributes['cols']:
                    raise AttributeError("different images have not the same size")
                # Same machine or frame of reference
                # How to define a 3D sequence or a time series
                ou = ou[np.newaxis, :, :]
                output_units = np.vstack([output_units, ou])
            # get slice position (relative to the origin)
            z_pos = self.get_z_position(dicom_file, im_pos[2])
            if z_pos is None:
                z_pos = i
            z_positions.append(z_pos)
            i += 1
            # self.updated.emit(i)
            self.updated.emit(message_text)
        # range the slices upon axis positions (only on 3d images)
        # ...actually, axis positions is not well defined
        # idx = np.argsort(axis_positions)
        # idx = idx[::-1]
        # output_units2 = np.copy(output_units)
        # for i in range(n_images):
        #     output_units2[i] = output_units[idx[i], :, :]
        # # That's it
        # dicom_image.set_pixel_values(output_units2)
        # A single 3D file has only one z_position...must define the rest of z_positions
        if len(self.files2open) == 1 and self.is_sequence and cs_xy is not None and slice_thickness is not None:
            c = dicom_image.attributes['cosines']
            # get z component of k' = i' x j'
            delta_z = -(c[0] * c[4] - c[1] * c[3])
            for i in range(1, n_images):
                z_positions.append(z_positions[0] + delta_z * slice_thickness * i)
        logging.info("image origin: " + str(im_pos))
        logging.info("voxel size (%f, %f, %f): " % (px_spacing[0], px_spacing[1], slice_thickness))
        logging.info("slice locations" + str(z_positions))
        dicom_image.set_pixel_values(output_units)
        dicom_image.set_slice_locations(z_positions)
        self.completed.emit([dicom_image])
        return

    @staticmethod
    def get_z_position(data_set, z_origin):
        # If SliceLocation exists is the easiest way to locate the slice
        keyword = {'SliceLocation': None, 'ImagePositionPatient': 2}
        for k in keyword.keys():
            element, path = tools.in_(data_set, k)
            if element is not None:
                # z must be relative to the origin
                z_rel = float(element.value[keyword[k]]) - z_origin
                return z_rel
        return None

    @staticmethod
    def get_date_time_acquisition(data_set):
        if 'AcquisitionDateTime' in data_set:
            dt = data_set.AcquisitionDateTime
            dt = dt.split(".")
            dt = dt[0]
            d = PyQt4.QtCore.QDate(int(dt[0:4]), int(dt[4:6]), int(dt[6:8]))
            t = PyQt4.QtCore.QTime(int(dt[8:10]), int(dt[10:12]), int(dt[12:]))
        if 'AcquisitionTime' in data_set:
            t = data_set.AcquisitionTime
            t = t.split(".")
            t = t[0]
            t = PyQt4.QtCore.QTime(int(t[0:2]), int(t[2:4]), int(t[4:]))
        if 'AcquisitionDate' in data_set:
            d = data_set.AcquisitionDate
            d = PyQt4.QtCore.QDate(int(d[0:4]), int(d[4:6]), int(d[6:]))
        return d, t

    @staticmethod
    def complement2(memory_value, base):
        """
        Get the negative value with a 2-complement given by the first parameter
        in a binary length defined by the second parameter:
        - From memory value to negative value C2(a,16)=-[not(a-1) & 0xffff]
        - From  negative valueC2 to memory value C2(b,16)= [not(-b) & 0xffff]+1
        """
        return -(~(memory_value - 1) & (2 ** base - 1))

    def __del__(self):
        self.quit()