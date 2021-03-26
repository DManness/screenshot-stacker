#!/usr/bin/env python3

import os
import sys
import requests
from PIL.ImageQt import ImageQt
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt, QTranslator, Signal, QObject, QThread, QThreadPool
from Presentation.gui_mainwindow import Ui_MainWindow
import configparser
import tempfile
from Model.ImageSorterModel import ImageSorterModel
import Controller
import logging
import argparse
import glob

import time

THUMBNAIL_SIZE = 32
CONFIG_FILE_PATH = 'config.ini'
STR_FILE_DIALOG_FILTER = 'Images (*.jpg *.jpeg *.jfif *.png *.tiff *tif *.bmp *.gif );;All Files (*)'


class MainWindow(QtWidgets.QMainWindow):
    """
    Main Screenshot Stacker application class wrapper. Hosts the controller class that interacts
    with the presentation class.
    """

    def __init__(self, parent=None, flags=Qt.WindowFlags(), open_files=[], verbose=False, **kwargs):
        """
        Construct a new Main Application Window.
        :param parent: the QObject that owns this item.
        :param flags: The window flags to be applied.
        """
        super(MainWindow, self).__init__(parent, flags)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig()
        self.logger.setLevel(logging.DEBUG if verbose else logging.WARN)

        self.logger.debug("Building UI")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = ImageSorterModel(self)
        self.ui.btn_preview.clicked.connect(self.btn_preview_clicked)
        self.ui.btn_export.clicked.connect(self.btn_export_clicked)
        self.ui.btn_save_as_browse.clicked.connect(self.btn_save_as_browse_clicked)

        self.ui.lst_file_list.setModel(self.model)
        self.ui.lst_file_list.setViewMode(QtWidgets.QListView.ViewMode.ListMode)

        # Buttons on the composition thumbnail list.
        self.ui.btn_img_add.clicked.connect(self.btn_img_add_clicked)
        self.ui.btn_img_remove.clicked.connect(self.btn_img_remove_clicked)
        self.ui.btn_img_move_up.clicked.connect(self.btn_img_move_up_clicked)
        self.ui.btn_img_move_down.clicked.connect(self.btn_img_move_down_clicked)

        self.ui.opt_orientation_horizontal.toggled.connect(self.opt_orientation_check_changed)

        for file_path in open_files:
            self.model.add_item(self._open_image(file_path))

        self._set_alignment(kwargs.get('alignment'))
        self._set_orientation(kwargs.get('orientation'))
        kwargs.get('output_path')

    def _set_orientation(self, orientation):
        if orientation == 'horizontal':
            self.ui.opt_orientation_horizontal.setChecked(True)
        else:
            self.ui.opt_orientation_vertical.setChecked(True)

    def _set_alignment(self, alignment):
        if alignment == 'center':
            self.ui.opt_align_center.setChecked(True)
        elif alignment == 'right':
            self.ui.opt_align_right.setChecked(True)
        else:
            self.ui.opt_align_left.setChecked(True)

    def opt_orientation_check_changed(self):
        """
        Changes the UI text on the alignment options to be more relevant to the selected orientation.
        :return: None
        """
        if self.ui.opt_orientation_horizontal.isChecked():
            self.ui.opt_align_left.setText(self.tr('Top'))
            self.ui.opt_align_center.setText(self.tr('Middle'))
            self.ui.opt_align_right.setText(self.tr('Bottom'))
        else:
            self.ui.opt_align_left.setText(self.tr('Left'))
            self.ui.opt_align_center.setText(self.tr('Center'))
            self.ui.opt_align_right.setText(self.tr('Right'))

    def btn_save_as_browse_clicked(self):
        """
        Prompts the user to select a path to save the composition.
        :return: None
        """
        open_dialog = QtWidgets.QFileDialog(self, "Save Image")
        open_dialog.setAcceptMode(open_dialog.AcceptSave)
        open_dialog.setFileMode(open_dialog.AnyFile)
        open_dialog.setConfirmOverwrite(False)
        open_dialog.setNameFilter(self.tr(STR_FILE_DIALOG_FILTER))
        open_dialog.open()
        if open_dialog.exec_():
            file_name = open_dialog.selectedFiles()[0] if open_dialog.selectedFiles() is not None else ""
            self.ui.txt_save_as_path.setText(file_name)

    def btn_img_add_clicked(self):
        """
        Prompts the user to select one or more images to add to the model.
        :return: None
        """
        open_dialog = QtWidgets.QFileDialog(self, self.tr("Open Image"))
        open_dialog.setFileMode(open_dialog.ExistingFiles)
        open_dialog.setNameFilter(self.tr(STR_FILE_DIALOG_FILTER))
        open_dialog.open()
        if open_dialog.exec_():
            file_names = open_dialog.selectedFiles()
            print(file_names)
            self._set_wait_cursor(True)
            for f in file_names:
                img = self._open_image(f)
                if img is not None:
                    self.model.add_item(img)
            self._set_wait_cursor(False)
        pass

    def btn_img_remove_clicked(self):
        if self.model.rowCount() > 0:
            cur_index = self.ui.lst_file_list.currentIndex()
            self.model.removeRows(cur_index.row(), 1)

    def btn_img_move_up_clicked(self):
        """
        Swaps the currently selected thumbnail with the previous item in the model, moving it up the list.
        :return: None
        """
        if self.model.rowCount() > 0:
            cur_index = self.ui.lst_file_list.currentIndex()
            if cur_index.row() > 0:
                self.model.move_up(cur_index.row())
                new_index = self.model.createIndex(cur_index.row() - 1, cur_index.row())
                self.ui.lst_file_list.setCurrentIndex(new_index)

        pass

    def btn_img_move_down_clicked(self):
        """
        Swaps the currently selected thumbnail with the next item in the model, moving it down the list.
        :return: None
        """
        if self.model.rowCount() > 0:
            cur_index = self.ui.lst_file_list.currentIndex()
            if cur_index.row() < self.model.rowCount() - 1:
                self.model.move_down(cur_index.row())
                new_index = self.model.createIndex(cur_index.row() + 1, cur_index.row())
                self.ui.lst_file_list.setCurrentIndex(new_index)

        pass

    def _open_image(self, image):
        """
        Tries to open an image for building the composition.
        :param image: The absolute path to the image to be opened.
        :returns:
            - Model.ImageThumbItem - A model class that stores the path, name, and thumbnail for the image.
            - None - If a particular image could not be opened.
        """
        try:
            return Controller.create_thumb_item(image, size=THUMBNAIL_SIZE)
        except FileNotFoundError as exp:
            QtWidgets.QMessageBox.warning(self, 'Warning', f'Could not open {image}')
            self.logger.warning(f'FAILED OPEN IMAGE \n{exp.with_traceback()}')
        except Exception as exp:
            QtWidgets.QMessageBox.warning(self, "Warning", f'Could not open {image}')
            self.logger.warning(f'FAILED OPEN IMAGE \n{exp.with_traceback()}')

    def _get_selected_alignment(self):
        """
        Get a flag literal for the alignment option depending on which item is currently selected.
        TODO: Replace the string literal with an enumeration or an int flag.
        :return: str either 'left', 'right' or 'center' - Note: these options apply regardless of the orientation.
        """
        if self.ui.opt_align_left.isChecked():
            return 'left'
        elif self.ui.opt_align_right.isChecked():
            return 'right'
        else:
            return 'center'

    def _get_selected_orientation(self):
        """
        Get a flag literal for the orientation option depending on which item is currently selected.
        TODO: Replace the string literal with an enumeration or an int flag.
        :return: str either 'horizontal' or 'vertical'
        """
        if self.ui.opt_orientation_horizontal.isChecked():
            return 'horizontal'
        else:
            return 'vertical'

    def btn_preview_clicked(self):
        """
        Generates a preview image.
        :return: None
        """
        self._set_wait_cursor(True)
        if self.model.rowCount() > 0:
            self.logger.debug('Creating full size composition and storing in memory.')
            self.full_composite_image = Controller.create_composite_image(self.model.imageList,
                                                  orientation=self._get_selected_orientation(),
                                                  alignment=self._get_selected_alignment())
            self.logger.debug('Creating preview sized image and storing in memory.')
            preview_sized_image = self.full_composite_image.reduce(2)
            self.ui.img_preview.setPixmap(preview_sized_image.toqpixmap())
        else:
            self.logger.debug('No images in composition.')
            QtWidgets.QMessageBox.information(self, "Information",
                                              "You must add at least 1 image to the composition before you can preview.")
        self._set_wait_cursor(False)

    def _save_image(self, export_path):
        """
        Logic to save the composition as an image.
        :param export_path: The absolute path to export the image.
        :return: None
        """
        self.logger.debug(f'Saving as "{export_path}".')
        try:
            with open(export_path, 'wb') as file_handle:
                self.full_composite_image.save(file_handle)
            self.logger.debug('File has been exported to disk.')
        except Exception as exp:
            self.logger.error(f"Failed to export image.\n{exp.with_traceback()}")
            QtWidgets.QMessageBox.critical(self, "Error",
                                           f'Failed to export the image.\nMessage:f{exp.with_traceback()}')

    def _set_wait_cursor(self, should_show_wait=True):
        """
        Private function that toggles the wait cursor for the application on or off.
        :param should_show_wait: True to display a wait cursor, False to display an arrow cursor.
        :return: None
        """
        self.ui.centralwidget.setCursor(
            QtGui.Qt.WaitCursor if should_show_wait else QtGui.Qt.ArrowCursor)

    def btn_export_clicked(self):
        """
        Handles the logic of exporting the image, prompting the user when input is needed.
        :return: None
        """
        if self.model.rowCount() > 0:
            self.logger.debug("Starting export.")
            export_path = os.path.abspath(self.ui.txt_save_as_path.text().strip())
            if os.path.exists(export_path) and os.path.isfile(export_path):
                self.logger.debug("File already exists. Prompt for overwrite.")
                ans = QtWidgets.QMessageBox.question(self, "Overwrite?",
                                                     f'The file "{export_path}" already exists. Do you want to replace it?',
                                                     defaultButton=QtWidgets.QMessageBox.No)
                self.logger.debug(f"User chose {ans.__str__()}.")
                if ans == QtWidgets.QMessageBox.Yes:
                    self._save_image(export_path)

            elif os.path.exists(export_path):
                self.logger.debug("User provided a directory. Using {TODO} as the file name.")
                print("TODO: Some path magic")
            else:
                self._save_image(export_path)
        else:
            self.logger.debug("Nothing to do. No images in composition.")
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
    with open(CONFIG_FILE_PATH, 'w') as cfgfile:
        config.write(cfgfile)

def in_str(string, value):
    try:
        string.index(value)
        return True
    except ValueError:
        return False

def configure_args():
    arg_parser.add_argument('-i', '--interactive', help='Open the GUI to load the existing images.', action='store_true')
    arg_parser.add_argument('-s', '--show', help='Opens the composition in the system viewer instead of saving to a file.', action='store_true')
    #arg_parser.add_argument('-l', '--log', help='Write logs to file (default is stdout, stderr)')
    #arg_parser.add_argument('-L', '--log_level', help='Sets the program\'s log level', action='store_true')
    arg_parser.add_argument('-v',  '--verbose', help='Increase the amount of console output.', action='store_true')
    arg_parser.add_argument('files', help='The path to one or more image files to be loaded.', nargs='*')
    arg_parser.add_argument('-a', '--alignment', default='left', help="(T)op, (M)iddle, (B)ottom, (L)eft, (C)enter, (R)ight")
    arg_parser.add_argument('-d', '--orientation', default='vertical', help="(H)orizontal or (V)ertical" )
    arg_parser.add_argument('-o', '--output', help="Output to the specified file.")


def parse_arg_alignment(raw_arg):
    DEFAULT = 'center'
    raw_arg = raw_arg.strip().lower()
    if len(raw_arg) > 0:
        a_letter = raw_arg[0]
    else:
        a_letter = DEFAULT[0]

    if a_letter == 'l' or a_letter == 't':
        alignment = 'left'
    elif a_letter == 'c' or a_letter == 'm':
        alignment = 'center'
    elif a_letter == 'r' or a_letter == 'b':
        alignment = 'right'
    return alignment

    pass
def parse_arg_orientation(raw_arg):
    raw_arg = raw_arg.strip().lower()
    if len(raw_arg) > 0 and raw_arg[0] == 'h':
        return 'horizontal'
    else:
        return 'vertical'

def parse_arg_outpath(raw_arg):
    return os.path.join(os.path.curdir, f'{int(time.time())}.png')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    configure_args()
    args = arg_parser.parse_args()
    if len([i for i in args.files if in_str(i, '*') ]) > 0:
        print('Globbing ("*") is not supported. Please use exact paths only.')
        #exit()
    #
    # if not os.path.exists(CONFIG_FILE_PATH):
    #     write_default_config()
    # config = configparser.ConfigParser()
    # config.read(CONFIG_FILE_PATH)

    # translator = QTranslator()
    # translator.load('i18n/fr_ca')
    extra_options = {
        'orientation': parse_arg_orientation(args.orientation),
        'alignment': parse_arg_alignment(args.alignment),
        'output_path': parse_arg_outpath(args.output),
        'verbose': args.verbose,
    }

    app = QtWidgets.QApplication(sys.argv)

    # QtWidgets.QStyleFactory.keys()
    #app.setStyle(config['DEFAULT']['style'])
    # app.installTranslator(translator)

    window = MainWindow(open_files=args.files, **extra_options)

    window.show()

    sys.exit(app.exec_())
