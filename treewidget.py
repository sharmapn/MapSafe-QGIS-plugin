import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

MIN__COLUMN, MAX__COLUMN = 1, 3


class Delegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        return editor

    def setEditorData(self, editor, index):
        md = index.model()

        if index.column() == MIN__COLUMN:
            ix = md.sibling(index.row(), MAX__COLUMN, index)
            editor.setMaximum(float(ix.data()))
            editor.setMinimum(-sys.float_info.max)

        elif index.column() == MAX__COLUMN:
            ix = md.sibling(index.row(), MIN__COLUMN, index)
            editor.setMinimum(float(ix.data()))
            editor.setMaximum(sys.float_info.max)

        editor.setValue(float(index.data()))


class Widget(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=None)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setItemDelegate(Delegate(self.tree_widget))
        self.tree_widget.setHeaderLabels(["Expresion Name", "Min", "Init", "Max", "Count"])
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.on_customContextMenuRequested)

        self.setCentralWidget(self.tree_widget)

        for vals in [("h", "20.0", "40.0", "60.0", "2"), ("k", "25.0", "50.0", "75.0", "2")]:
            it = QTreeWidgetItem(vals)
            it.setFlags(it.flags()| Qt.ItemIsEditable)
            self.tree_widget.addTopLevelItem(it)

    def on_customContextMenuRequested(self, pos):
        selected_item = self.tree_widget.itemAt(pos)
        menu = QMenu()
        min_action = menu.addAction("Edit Min")
        max_action = menu.addAction("Edit Max")
        action = menu.exec_(self.tree_widget.viewport().mapToGlobal(pos))
        if action == min_action:
            self.tree_widget.editItem(selected_item, MIN__COLUMN)
        elif action == max_action:
            self.tree_widget.editItem(selected_item, MAX__COLUMN)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())