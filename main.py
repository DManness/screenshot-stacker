#!/usr/bin/env python3

import os
import sys
import requests
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt, QTranslator, Signal, QObject, QThread, QThreadPool
from gui_mainwindow import Ui_MainWindow
from PIL import Image
from PIL.ImageQt import ImageQt
import configparser
import tempfile

THUMBNAIL_SIZE = 32
CONFIG_FILE_PATH = 'config.ini'


class ImageSorterModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(ImageSorterModel, self).__init__(parent)
        self.imageCount = 0
        self.imageList = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.imageList)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if index.row() >= len(self.imageList) or index.row() < 0:
            return None
        if role == QtCore.Qt.DisplayRole:
            return self.imageList[index.row()].display_name
        if role == QtCore.Qt.ItemDataRole:
            return self.imageList[index.row()]
        if role == QtCore.Qt.DecorationRole:
            return self.imageList[index.row()].get_thumbnail()
        return None

    def add_item(self, item):
        if not isinstance(item, ImageThumbItem):
            raise ValueError("You done goofed")
        self.imageList.append(item)
        self.imageCount += 1
        self.layoutChanged.emit()

    def move_up(self, item):
        self.layoutAboutToBeChanged.emit()
        self.imageList.index(item)
        self.changePersistentIndexList()
        self.layoutChanged.emit()

    def insertRows(self, position, rows, index=QtCore.QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)

        for row in range(0,rows):
            self.imageList.insert(position, self.add_item(row))

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, index=QtCore.QModelIndex()):
        self.beginRemoveRows(index, position, position + rows - 1)

        for row in range(0, rows):
            del self.imageList[position]

        self.endRemoveRows()
        return True
        pass


class ImageThumbItem(object):

    def __init__(self, display_name, fulll_name, thumbnail):
        self.display_name = display_name
        self.full_name = fulll_name
        self.thumbnail = thumbnail

        #if not os.path.exists("__cache"):
        #    os.mkdir("__cache")
        #thumbnail.save(f"__cache/{self.display_name}")
        #self.q_thumb = QtGui.QIcon(f"__cache/{self.display_name}")

        self.q_thumb = self.thumbnail.toqpixmap()

    def get_thumbnail(self):
        return self.q_thumb
        #return self.q_thumb


def smart_crop_image(image_handle):
    width, height = image_handle.size
    if height > width:
        adjust = int((height - width) / 2)
        box = (0, adjust, width, height - adjust)
    else:
        adjust = int((width - height) / 2)
        box = (adjust, 0, width - adjust, height)

    return image_handle.crop(box)


def create_thumbnail(image_path, size=64):
    image = open(image_path, 'rb')
    thumb = smart_crop_image(Image.open(image))

    thumb.thumbnail((size, size))
    image.close()
    return thumb


def create_thumb_item(image_path, size=64):
    full_path = os.path.abspath(image_path)
    base_name = os.path.basename(full_path)
    thumb = create_thumbnail(full_path, size=size)
    return ImageThumbItem(base_name, full_path, thumb)


def create_composite_image(image_array, orientation='vertical', alignment='left'):
    is_vert = orientation == 'vertical'
    out_size_v = 0
    out_size_h = 0
    largest_width = 0
    largest_height = 0
    # This first round discovers information about each file provided.
    for img in image_array:
        with open(img.full_name, 'rb') as file_pointer:
            img_handle = Image.open( file_pointer )
            out_size_v += img_handle.height
            out_size_h += img_handle.width
            largest_width = max(largest_width, img_handle.width )
            largest_height = max(largest_height, img_handle.height )

    if is_vert:
        out_image = Image.new('RGB', (largest_width, out_size_v) )
    else:
        out_image = Image.new('RGB', (out_size_h, largest_height))
    img_cursor = 0
    for img in image_array:
        with open(img.full_name, 'rb') as file_pointer:
            img_handle = Image.open(file_pointer).convert('RGB')

            if is_vert:
                if alignment == 'left':
                    x_offset = 0
                elif alignment == 'right':
                    x_offset = largest_width - img_handle.width
                else:
                    x_offset = int((largest_width - img_handle.width) / 2)

                out_image.paste(img_handle, box=(x_offset, img_cursor,
                                                 img_handle.width + x_offset, img_handle.height + img_cursor))
                img_cursor += img_handle.height
            else:

                if alignment == 'left':
                    y_offset = 0
                elif alignment == 'right':
                    y_offset = largest_height - img_handle.height
                else:
                    y_offset = int((largest_height - img_handle.height) / 2)

                out_image.paste(img_handle, box=(img_cursor, y_offset,
                                                 img_handle.width + img_cursor, img_handle.height + y_offset))
                img_cursor += img_handle.width
    return out_image




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(MainWindow, self).__init__(parent, flags)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = ImageSorterModel(self)
        test = self._open_image(r'sample.png')
        i_to_a = []
        if test is not None:
            i_to_a.append(test)
        self.i_to_a = i_to_a
        self.ui.btn_preview.clicked.connect(self.btn_preview_clicked)
        self.ui.btn_export.clicked.connect(self.btn_export_clicked)
        for i in i_to_a:
            self.model.add_item(i)
        self.ui.lst_file_list.setModel(self.model)
        self.ui.lst_file_list.setViewMode(QtWidgets.QListView.ViewMode.ListMode)

        self.ui.btn_img_add.clicked.connect(self.btn_img_add_clicked)
        self.ui.btn_img_remove.clicked.connect(self.btn_img_remove_clicked)
        self.ui.btn_img_move_up.clicked.connect(self.btn_img_move_up_clicked)
        self.ui.btn_img_move_down.clicked.connect(self.btn_img_move_down_clicked)
        self.ui.btn_save_as_browse.clicked.connect(self.btn_save_as_browse_clicked)

    def btn_save_as_browse_clicked(self):
        open_dialog = QtWidgets.QFileDialog(self, "Save Image")
        open_dialog.setAcceptMode(open_dialog.AcceptSave)
        open_dialog.setFileMode(open_dialog.AnyFile)
        open_dialog.setConfirmOverwrite(False)
        open_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.tiff *tif *.bmp *.gif );;All Files (*)")
        open_dialog.open()
        if open_dialog.exec_():
            file_name = open_dialog.selectedFiles()[0] if open_dialog.selectedFiles() is not None else ""
            self.ui.txt_save_as_path.setText(file_name)

    def btn_img_add_clicked(self):
        open_dialog = QtWidgets.QFileDialog(self, "Open Image")
        open_dialog.setFileMode(open_dialog.ExistingFiles)
        open_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.tiff *tif *.bmp *.gif );;All Files (*)")
        open_dialog.open()
        if open_dialog.exec_():
            file_names = open_dialog.selectedFiles()
            for f in file_names:
                img = self._open_image(f)
                if img is not None:
                    self.model.add_item(img)
        pass

    def btn_img_remove_clicked(self):
        pass

    def btn_img_move_up_clicked(self):
        pass

    def btn_img_move_down_clicked(self):
        pass

    def _open_image(self, image):
        try:
            return create_thumb_item(image, size=THUMBNAIL_SIZE)
        except FileNotFoundError as exp:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Could not open {image}")
        except Exception as exp:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Could not open {image}")


    def _get_selected_alignment(self):
        if self.ui.opt_align_left.isChecked():
            return 'left'
        elif self.ui.opt_align_right.isChecked():
            return 'right'
        else:
            return 'center'

    def _get_selected_orientation(self):
        if self.ui.opt_orientation_horizontal.isChecked():
            return 'horizontal'
        else:
            return 'vertical'

    def btn_preview_clicked(self):
        if self.model.rowCount() > 0:
            self.beefull = create_composite_image(self.model.imageList,
                                             orientation=self._get_selected_orientation(),
                                             alignment=self._get_selected_alignment())
            beacon = self.beefull.reduce(2)
            tester = ImageQt(beacon)
            self.ui.img_preview.setPixmap(beacon.toqpixmap())
        else:
            QtWidgets.QMessageBox.information(self, "Information",
                                              "You must add at least 1 image to the composition before you can preview.")

    def _save_image(self, export_path):
        try:
            with open(export_path, 'wb') as file_handle:
                self.beefull.save(file_handle)
        except Exception as exp:
            QtWidgets.QMessageBox.critical(self, "Error",
                                           f'Failed to export the image.\nMessage:f{exp.with_traceback()}')

    def btn_export_clicked(self):
        if self.model.rowCount() > 0:
            print("exporting")
            export_path = os.path.abspath(self.ui.txt_save_as_path.text().strip())
            if os.path.exists(export_path) and os.path.isfile(export_path):
                ans = QtWidgets.QMessageBox.question(self, "Overwrite?",
                                                     f'The file "{export_path}" already exists. Do you want to replace it?',
                                                     defaultButton=QtWidgets.QMessageBox.No)
                if ans == QtWidgets.QMessageBox.Yes:
                    self._save_image(export_path)

            elif os.path.exists(export_path):
                print("TODO: Some path magic")
            else:
                self._save_image(export_path)
        else:
            QtWidgets.QMessageBox.information(self, "Information",
                                              "You must add at least 1 image to the composition before you can export.")

# Signals must inherit QObject
class ProgressSignals(QObject):
    progress = Signal(object)
    error = Signal(object)
    complete = Signal(object)


# Create the Worker Thread
class WorkerThread(QThread):
    def __init__(self, command, *args, parent=None):
        QThread.__init__(self, parent)
        # Instantiate signals and connect signals to the slots
        self.signals = ProgressSignals()

    def run(self):
        # Do something on the worker thread
        a = 1 + 1
        # Emit signals whenever you want
        try:

            self.signals.complete.emit({})
        except Exception as exp:
            self.signals.error.emit(exp)


def write_default_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'style': 'Fusion',
        'log_level': 'info',
        'background_color': "000"
    }
    with open (CONFIG_FILE_PATH, 'w') as cfgfile:
        config.write(cfgfile)


if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE_PATH):
        write_default_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    #translator = QTranslator()
    #translator.load('i18n/fr_ca')
    app = QtWidgets.QApplication(sys.argv)

    #QtWidgets.QStyleFactory.keys()
    app.setStyle(config['DEFAULT']['style'])
    #app.installTranslator(translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
