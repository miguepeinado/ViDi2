#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import PyQt4.QtCore
import PyQt4.QtGui


__author__ = "M.A. Peinado"
__copyright__ = "2016, M.A. Peinado"
__credits__ = ["Miguel A. Peinado"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "M.A. Peinado"
__email__ = "miguel.peinado@sespa.es"
__status__ = "prototype"


class DicomImage:
    """
    Encapsulates the image and most relevant data of a dicom dataset or a series of data set.

    Attributes
        - is sequence: Defines if the dataset(s) are independent images from the same machine
        - is_overlay: Defines if the dataset(s) is the overlay of an hybrid image system (SPECT/CT, PET/CT...)

        - current_index: Actual image number. Useful for painting the image
        - attributes: Dict with most relevant data if the dataset(s) excluding pixel values (modality, machine UID,
                      info about image representation (byte storage configuration, samples per pixels, padding, lut...)
            * rows: Rows of the image assumed is planar
            * cols: Rows of the image assumed is planar
            * n_images: Number of images of the dataset assumed is planar. For 3D images this take no information about
                    orientation of the planes
            * center, window: center and window of an image
            * allocated, stored, high_bit, samples_per_pixel, data_type, pixel_units, padding_value, inverted,
                    cfr_uid, cs_xy slice_thickness, im_pos, px_spacing
        - color_table: Defined color voi_table for the dataset(s). Useful also for hybrid images where they are painted in
                       watershed over the "base" modality (CT/MR)
    """
    # todo define a new dataset as pydicom.dataset + pixel_values???
    def __init__(self):
        self.is_sequence = False
        self.is_overlay = False
        self.current_index = 0
        self.attributes = {}
        self.color_table = []
        self._pixel_values = None
        self.slice_locations = []
        self.lowest_value = None
        self.highest_value = None
        self.low_value = None
        self.high_value = None
        self.alpha = 92

#
# <---------------- Setters/getters ------------------------>
#
# ...Attributes
    def set_attributes(self, attributes):
        self.attributes = attributes

    def get_info(self):
        z = self.to_ref_frame([PyQt4.QtCore.QPointF(0, 0)])
        return {'z': z[0][2], 'index': self.current_index, 'total': len(self.slice_locations),
                'window': self.attributes['window'], 'center': self.attributes['center'],
                'patient_data': self.attributes['patient_data'], 'acq_date_time': self.attributes['acq_date_time']}

# ...Slice location

    def get_current_z_position(self):
        """Gets the location (z) of the actual slice"""
        return self.slice_locations[self.current_index]

    def set_slice_locations(self, locations):
        self.slice_locations = locations

    def get_nearest_location(self, z):
        """Get the nearest slice location for a position"""
        ix = -1
        diff = 1.e7
        i = 0
        for l in self.slice_locations:
            if abs(l - z) <= diff:
                ix = i
                diff = abs(l - z)
            i += 1
        return ix, self.slice_locations[ix]

#
# ...Pixel values
#
    def pixel_values(self):
        return self._pixel_values

    def pixel_values_for_index(self, n_z):
        return self._pixel_values[n_z, :, :]

    def value_at(self, x, y):
        if 0 <= x < self._pixel_values.shape[2] and 0 <= y < self._pixel_values.shape[1]:
            x = int(x)
            y = int(y)
            return self._pixel_values[self.current_index, y, x]

    def pixmap(self):
        pv = self._pixel_values[self.current_index, :, :]
        # np.savetxt('/home/migue/Escritorio/pixel-values.csv', pv.astype(np.int16), delimiter=",", fmt='%s')
        # Calculate LUT values if not present and needed (W/C)
        # todo: For what needsLUT is worth?
        self.needsLUT, window, center = self.lut_values(pv, self.attributes['window'],
                                                        self.attributes['center'])
        # From http://www.swharden.com/wp/2013-06-03-realtime-image-pixelmap-from-numpy-array-data-in-qt/
        pv = self.values_after_lut(pv, window, center)
        pv = np.require(pv, np.uint8, 'C')
        qt_image = PyQt4.QtGui.QImage(pv.data, self.attributes['cols'], self.attributes['rows'],
                                      PyQt4.QtGui.QImage.Format_Indexed8)
        qt_image.setColorTable(self.color_table)
        return PyQt4.QtGui.QPixmap.fromImage(qt_image)

    def pixel_limits(self):
        ii = np.iinfo(self.attributes['data_type'])
        l = ii.min
        u = ii.max
        return l, u

    def pixel_thresholds(self):
        if self.lowest_value is None:
            self.lowest_value = np.nanmin(self._pixel_values)
            self.low_value = self.lowest_value
            self.highest_value = np.nanmax(self._pixel_values)
            self.high_value = self.highest_value
        return self.low_value, self.high_value

    def set_threshold(self, low, high):
        self.low_value = low
        self.high_value = high

    def next_image(self):
        self.current_index += 1
        if self.current_index == self.attributes['n_images']:
            self.current_index -= 1
        return self.current_index, self.pixmap()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
        return self.current_index, self.pixmap()

    def pixmap_for_location(self, z):
        self.current_index, _ = self.get_nearest_location(z)
        return self.pixmap()

    def pixmap_for_index(self, n_z):
        self.current_index = n_z
        return self.pixmap()

    def set_pixel_values(self, array):
        self._pixel_values = array

#
# <---------------- pixel representation ------------------------>
#
    def set_default_color_table(self):
        self.color_table = []
        for i in range(256):
            ii = (255 - i) if (self.attributes['inverted'] or self.attributes['pixel_units'] == 'OD') else i
            if self.is_overlay:
                ii = (255 - i)
                self.color_table.append(PyQt4.QtGui.QColor.fromHsl(ii, 255, 128, self.alpha).rgba())
            else:
                self.color_table.append(PyQt4.QtGui.qRgb(ii, ii, ii))
        # In overlays set zero value to transparent
        if self.is_overlay:
            self.color_table[0] = PyQt4.QtGui.QColor.fromRgb(0, 0, 0, alpha=0).rgba()

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_default_color_table()

    def set_wl(self, window, center):
        self.attributes['window'] = window
        self.attributes['center'] = center

    def lut_values(self, pxx, window, center):
        """Determine if the image has or needs a LUT and the window and center"""
        # Sometimes modality defines a maximum and minimum absolute values
        needsLUT = (self.attributes['allocated'] > 8) and (self.attributes['samples_per_pixel'] == 1)
        # Minimum and maximum values excepted NaN (padded) values
        px2 = np.where(pxx == self.attributes['padVal'], np.NaN, pxx) if (self.attributes['padVal'] is not None) \
            else pxx

        self.pixel_thresholds()
        # if it's an overlay override window and center
        if (window is None) or (center is None) or self.is_overlay:
            center = (self.low_value + self.high_value) / 2.0
            window = (self.high_value - self.low_value)
        return needsLUT, window, center

    def values_after_lut(self, data, window, center):
        """Apply the Look-Up Table for the given data and window/level value"""
        low_limit = (center - 0.5 - (window - 1.0) / 2.0)
        high_limit = (center - 0.5 + (window - 1.0) / 2.0)
        # Change pad values to black
        px2 = np.copy(data)
        px3 = np.copy(data)
        px2[np.isnan(px2)] = low_limit - 1
        px3[np.isnan(px3)] = low_limit - 1
        px2[px2 < low_limit] = 0.
        px2[px2 > high_limit] = 0.
        px3 = np.piecewise(px3, [px3 < low_limit, px3 > high_limit],
                           [0, 255, lambda px: (((px - (center - 0.5)) / (window - 1.0) + 0.5) * 255.0)])
        return px3

#
# <---------------- Others ------------------------>
#
    def to_ref_frame(self, list_of_points, n_z=None):
        """Translate the 3D point in the dataset to the 'absolute' frame of coordinates

        :arg list_of_points: list of 2D point in a slice (QPointF)
        :arg n_z: slice location index (if none get the actual one)
        :return p: list with the coordinates of the 3D point
        """
        if n_z is None:
            n_z = self.current_index
        c = self.attributes['cosines']
        # lazily calculate cosines for z direction
        if len(c) == 6:
            cx = c[1] * c[5] - c[2] * c[4]
            cy = c[2] * c[3] - c[0] * c[5]
            cz = c[0] * c[4] - c[1] * c[3]
            c += [cx, cy, cz]
            self.attributes['cosines'] = c
        l = []
        for point in list_of_points:
            # 1. rescale
            p = [point.x() * self.attributes['pixel_spacing'][0], point.y() * self.attributes['pixel_spacing'][1],
                 self.slice_locations[n_z]]
            # 2. rotate
            p2 = [0] * 3
            for j in range(3):
                for i in range(3):
                    p2[j] += p[i] * c[i * 3 + j]
            # 3. translate
            l.append([p2[i] + self.attributes['origin'][i] for i in range(3)])
        return l

    def from_ref_frame(self, list_of_points):
        """Translate the 3D point in the dataset to the 'absolute' frame of coordinates

        NOTE: As data sets must be coplanar we don't need to deal with cosines and transform arrays
        :arg list_of_points: list with the points if form of 3D coordinates
        :return point, z: 2D point in a slice and slice location
        """
        # lazily calculate cosines for z direction
        c = self.attributes['cosines']
        if len(self.attributes['cosines']) == 6:
            c = self.attributes['cosines']
            cx = c[1] * c[5] - c[2] * c[4]
            cy = c[2] * c[3] - c[0] * c[5]
            cz = c[0] * c[4] - c[1] * c[3]
            c += [cx, cy, cz]
            self.attributes['cosines'] = c
        # For rotation must transpose cosine array
        c_t = c
        for i in range(9):
            a = i % 3
            b = i // 3
            j = b * 3 + a
            c_t[j] = c[i]
        qpf = []
        z = None
        for p in list_of_points:
            # 1. Translate
            op = [p[i] - self.attributes['origin'][i] for i in range(3)]
            # 2. Rotate
            p2 = [0] * 3
            for j in range(3):
                for i in range(3):
                    p2[j] += op[i] * c_t[i * 3 + j]
            # 3. Rescale
            qpf.append(PyQt4.QtCore.QPointF(p2[0] / self.attributes['pixel_spacing'][0],
                                            p2[1] / self.attributes['pixel_spacing'][1]))
            # Pay attention that z is in mm not in dataset units
            if z is None:
                z = p2[2]
            elif z != p2[2]:
                raise ValueError("Point are not coplanar")
        # points are assumed to be coplanar
        n_z, _ = self.get_nearest_location(z)
        return qpf, n_z
