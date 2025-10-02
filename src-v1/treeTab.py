from PySide6.QtWidgets import (
    QWidget,
    QTreeWidget,
    QHBoxLayout,
    QFileDialog,
    QTabWidget,
    QTreeWidgetItem,
    QPushButton,
    QMainWindow,
    QToolBar,
    QSplitter,
)
import os
from abstractAdapter import AbstractAdapter as AA
from fileSwitchOpener import file_switch_open

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

def get_arr(file_path: str):
    file_name, ext = os.path.basename(file_path).split('.')
    if file_name == '': file_name = 'untitled'
    ext = ext.upper()
    return [file_name, ext]

class TreeItem(QTreeWidgetItem):
    def __init__(self, arr, adapter: AA, parent: QTreeWidgetItem):
        super().__init__(arr)
        self.adapter = adapter
        self.p = parent
    
    def remove(self):
        self.p.addChildren(self.takeChildren())
        self.p.removeChild(self)

class TreeTab(QSplitter):
    def __init__(self, parent):
        super().__init__(parent)
        self.setOrientation(Qt.Orientation.Horizontal)

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Name', 'Type'])
        self.tree.itemClicked.connect(self.tree_item_clicked)

        self.tab = QTabWidget(self)
        self.tab.tabBar().hide()

        self.addWidget(self.tree)
        self.addWidget(self.tab)
    
    def tree_item_clicked(self, item: TreeItem, _):
        self.switch(item)

    def open_file(self, file_path: str):
        self.mount(file_path, self.tree.currentItem())

    def open_menu(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File",
            filter="All (*.md *.html *.txt);; Rich Text (*.md *.html);; Markdown (*.md);; HTML (*.html);; Text (*.txt)"
        )
        if os.path.isfile(file_path):
            self.mount(file_path)
        else:
            print('cancelled')
    
    def mount(self, file_path: str, parentItem: QTreeWidgetItem=None):
        if parentItem == None:
            parentItem = self.tree.invisibleRootItem()
        adapter = file_switch_open(file_path, link_handle=self.open_file)
        self.tab.addTab(adapter.get_widget(), "test")
        item = TreeItem(get_arr(file_path), adapter, parentItem)
        parentItem.addChild(item)
        self.switch(item)
    
    def switch(self, item: TreeItem):
        self.tree.setCurrentItem(item)
        self.tab.setCurrentIndex(self.tab.indexOf(item.adapter.get_widget()))
    
    def close_current(self):
        item: TreeItem = self.tree.currentItem()
        if item:
            self.tab.removeTab(self.tab.indexOf(item.adapter.get_widget()))
            item.remove()

    def save(self):
        item: TreeItem = self.tree.currentItem()
        if item:
            item.adapter.save()
    
    def save_as(self):
        item: TreeItem = self.tree.currentItem()
        if item:
            file_path = item.adapter.save_as()
            print(file_path)
            if file_path:
                f, e = get_arr(file_path)
                item.setText(0, f)
                item.setText(1, e)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        self.tab = TreeTab(self)
        self.setCentralWidget(self.tab)

        open_btn = QAction(text='Open', parent=self)
        open_btn.triggered.connect(self.tab.open_menu)
        toolbar.addAction(open_btn)

        new_md = QAction(text='New Markdown', parent=self)
        new_md.triggered.connect(lambda: self.tab.mount('.md'))
        toolbar.addAction(new_md)

        save_btn = QAction(text='Save', parent=self)
        save_btn.triggered.connect(self.tab.save)
        toolbar.addAction(save_btn)

        save_as_btn = QAction(text='Save As', parent=self)
        save_as_btn.triggered.connect(self.tab.save_as)
        toolbar.addAction(save_as_btn)

        close_btn = QAction(text='Close', parent=self)
        close_btn.triggered.connect(self.tab.close_current)
        toolbar.addAction(close_btn)
    
if __name__ == "__main__":
    import widgetTester

    def create_tree_tab():
        return Window()
    
    widgetTester.test('test tree tabs mounting', create_tree_tab)