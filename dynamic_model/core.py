import sqlite3
from sqlite3 import Error
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .ui.dynamicTableView import Ui_Form
from .listmodel import ListModel

try:
    conn = sqlite3.connect('/home/alexandr/PycharmProjects/Pocket/pocket_articles/data/articlesdb.sqlite')
except Error as e:
    print('Error database connection')
    print(e)
    sys.exit()

query = "select * from webpages"

cur = conn.execute(query)


# data = cur.fetchmany(10)
# while data:
#     print(len(data))
#     data = cur.fetchmany(10)
#
# if conn:
#     conn.close()


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.loadUI()

    def loadUI(self):
        self.model = ListModel(row_count=20)
        self.model.getData(cur)
        self.ui.tableView.setModel(self.model)
        self.g = self.model._generator()

        self.ui.tableView.doubleClicked.connect(self.doubleClick)

    def doubleClick(self):
        idx = self.ui.tableView.currentIndex()
        data = idx.data(Qt.UserRole)
        self.ui.textEdit.setText(str(data))
        try:
            self.ui.textEdit.setText(next(self.g))
        except StopIteration:
            self.stdout('exception')
            self.g = self.model._generator()
            self.ui.textEdit.setText(next(self.model._g))

    def stdout(self, txt):
        self.ui.textEdit.setText(txt)

    def closeEvent(self, event):
        cur.close()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    wgt = MainWidget()
    wgt.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
