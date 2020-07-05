from PySide2 import QtCore
from .ImageThumbItem import ImageThumbItem

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

    def move_up(self, position):
        self.layoutAboutToBeChanged.emit()
        self._swap_elements(position, position - 1)
        # self.changePersistentIndexList(position-1, position)
        self.layoutChanged.emit()

    def move_down(self, position):
        self.layoutAboutToBeChanged.emit()
        self._swap_elements(position, position + 1)
        # self.changePersistentIndexList(position-1, position)
        self.layoutChanged.emit()

    def insertRows(self, position, rows, index=QtCore.QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)

        for row in range(0, rows):
            self.imageList.insert(position, self.add_item(row))

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, index=QtCore.QModelIndex()):
        self.beginRemoveRows(index, position, position + rows - 1)

        for row in range(0, rows):
            del self.imageList[position]

        self.endRemoveRows()
        return True

    def _swap_elements(self, i_1, i_2):
        temp = self.imageList[i_1]
        self.imageList[i_1] = self.imageList[i_2]
        self.imageList[i_2] = temp
