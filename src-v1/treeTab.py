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

from PySide6.QtCore import QPersistentModelIndex

class TreeTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        button = QPushButton('Open File')
        button.clicked.connect(self.open_menu)

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Name', 'Type'])

        self.tabs = QTabWidget(self)
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(button)
        layout.addWidget(self.tree)
        layout.addWidget(self.tabs)

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
            self.mount(adapter)
    
    def mount(self, adapter: AA):
        file_name, ext = adapter.get_basename().split('.')
        ext = ext.upper()
        tree_item = QTreeWidgetItem([file_name, ext])
        self.tree.invisibleRootItem().addChild(tree_item)
        # tree_index = self.tree.indexFromItem(tree_item)
        # p_tree_index = QPersistentModelIndex(tree_index)

        self.tabs.addTab(adapter.get_widget(), 'test')
        # tab_index = self.tabs.indexOf(adapter.get_widget())
        # p_tab_index = QPersistentModelIndex(tab_index)

        # return (p_tree_index, p_tab_index)
    
if __name__ == "__main__":
    import widgetTester

    def create_tree_tab():
        return TreeTab(None)
    
    widgetTester.test('test tree tabs mounting', create_tree_tab)