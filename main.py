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

THUMBNAIL_SIZE = 128
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

        if not os.path.exists("__cache"):
            os.mkdir("__cache")
        thumbnail.save(f"__cache/{self.display_name}")
        self.q_thumb = QtGui.QIcon(f"__cache/{self.display_name}")

    def get_thumbnail(self):
        return self.q_thumb


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
        model = ImageSorterModel(self)
        i_to_a = [
            create_thumb_item(r'sample.png', size=THUMBNAIL_SIZE)
        ]
        self.i_to_a = i_to_a
        self.ui.btn_preview.clicked.connect(self.btn_preview_clicked)
        for i in i_to_a:
            model.add_item(i)
        self.boop = False
        self.ui.lst_file_list.setModel(model)
        self.ui.lst_file_list.setViewMode(QtWidgets.QListView.ViewMode.ListMode)

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
        beefull = create_composite_image(self.i_to_a,
                                         orientation=self._get_selected_orientation(),
                                         alignment=self._get_selected_alignment())
        beacon = beefull.reduce(2)
        #beacon.save("__cache/sample.jpg", "jpeg")

        #tester = QtGui.QPixmap(QtGui.QImage("__cache/sample.jpg"))
        tester = ImageQt(beacon)

        self.ui.img_preview.setPixmap(beacon.toqpixmap())
        self.boop = not self.boop

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
