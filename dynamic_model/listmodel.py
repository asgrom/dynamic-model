import typing

from PyQt5.QtCore import *
from sqlite3 import Cursor


class ListModel(QAbstractTableModel):
    def __init__(self, row_count, parent=None):
        super(ListModel, self).__init__(parent)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.row_count

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return f'row {index.row()}, column {index.column()}'
        return None

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def getData(self, cursor: Cursor):
        # Начинается операция сброса модели.
        # Операция сброса сбрасывает модель до ее текущего состояния в любых прикрепленных видах.
        self.beginResetModel()

        self._data = cursor.execute(self.query).fetchall()

        # Конец операции сброса
        self.endResetModel()

    def _generator(self):
        for i in range(self.row_count):
            yield f'generator {i}'

    def canFetchMore(self, parent: QModelIndex) -> bool:
        try:
            print('canFetchMore')
            next(self._g)
        except StopIteration:
            print('canFetchMore exception')
            return False
        else:
            return True

    def fetchMore(self, parent: QModelIndex) -> None:
        super().fetchMore(parent)
