from PySide6.QtWidgets import (
    QTreeWidget,
    QFileDialog,
    QTabWidget,
    QTreeWidgetItem,
    QSplitter,
)
import os
from abstractAdapter import AbstractAdapter as AA
from fileSwitchOpener import file_switch_open

from PySide6.QtCore import Qt

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

    def toggle_file_browser_visible(self):
        visible = not self.tree.isVisible()
        self.tree.setVisible(visible)
        return visible
    
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