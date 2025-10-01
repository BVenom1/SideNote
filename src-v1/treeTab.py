from PySide6.QtWidgets import (
    QWidget,
    QTreeWidget,
    QHBoxLayout,
    QFileDialog,
    QTabWidget,
    QTreeWidgetItem,
    QPushButton,
)
import os
from abstractAdapter import AbstractAdapter as AA

from PySide6.QtCore import QModelIndex, QPersistentModelIndex

class TreeItem(QTreeWidgetItem):
    def __init__(self, arr, adapter: AA):
        super().__init__(arr)
        self.adapter = adapter

class TreeTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        button = QPushButton('Open File')
        button.clicked.connect(self.open_menu)

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Name', 'Type'])
        self.tree.itemClicked.connect(self.tree_item_clicked)

        self.tab = QTabWidget(self)
        self.tab.tabBar().hide()

        self.tabs = set()
        
        self.l = QHBoxLayout()
        self.setLayout(self.l)

        self.l.addWidget(button)
        self.l.addWidget(self.tree)
        self.l.addWidget(self.tab)
    
    def tree_item_clicked(self, item: TreeItem, _):
        self.switch(item.adapter.get_widget())

    def open_file(self, file_path: str, parent: AA):
        print(f'requested {file_path} from {parent.get_basename()}')

    def open_menu(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File",
            filter="All (*.md *.html *.txt);; Rich Text (*.md *.html);; Markdown (*.md);; HTML (*.html);; Text (*.txt)"
        )
        if os.path.isfile(file_path):
            from fileSwitchOpener import fileSwitchOpen
            adapter = fileSwitchOpen(file_path, link_handle=self.open_file)
            self.tabs.add(adapter.get_widget())
            self.current_tab = adapter.get_widget()
            self.mount(adapter)
    
    def switch(self, widget: QWidget):
        index = self.tab.indexOf(widget)
        self.tab.setCurrentIndex(index)

    def mount(self, adapter: AA):
        file_name, ext = adapter.get_basename().split('.')
        ext = ext.upper()
        tree_item = TreeItem([file_name, ext], adapter)
        self.tree.invisibleRootItem().addChild(tree_item)
        new_widget = adapter.get_widget()
        self.tab.addTab(new_widget, "test")
        self.tabs.add(new_widget)
        self.switch(new_widget)
    
if __name__ == "__main__":
    import widgetTester

    def create_tree_tab():
        return TreeTab(None)
    
    widgetTester.test('test tree tabs mounting', create_tree_tab)