from PySide6.QtWidgets import (
    QTreeWidget,
    QTabWidget,
    QTreeWidgetItem,
    QSplitter,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QMenu,
)
import os
from adapter.abstractAdapter import AbstractAdapter as AA
from fileHandler import FileHandler

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction

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

class TreeTab(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_handle = FileHandler()

        # Tree style file broser ----------------------------------------------
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Name', 'Type'])
        self.tree.itemClicked.connect(self.tree_item_clicked)
        self.tree.setVisible(False)

        # Bar on top of the Tab -----------------------------------------------
        button_width = 30

        self.collapse_btn = QPushButton(self)
        self.collapse_btn.setIcon(QIcon('assets/chevron-right.svg'))
        self.collapse_btn.setFixedWidth(button_width)
        self.collapse_btn.clicked.connect(self.toggle_file_browser_visible)

        file_menu = QMenu('File', self)
        file_btn = QPushButton(self)
        file_btn.setIcon(QIcon('assets/menu.svg'))
        file_btn.setFixedWidth(button_width)
        file_btn.setMenu(file_menu)
        file_btn.setStyleSheet("QPushButton::menu-indicator { image: none; width: 0; }")

        self.add_to_menu('Open', file_menu, self.open_menu, 'Ctrl+O')
        self.add_to_menu('New Markdown', file_menu, lambda: self.open_file('.md'), 'Ctrl+M')
        self.add_to_menu('New Text', file_menu, lambda: self.open_file('.txt'), 'Ctrl+T')
        self.add_to_menu('Save', file_menu, self.save, 'Ctrl+S')
        self.add_to_menu('Save As', file_menu, self.save_as, 'Ctrl+A')

        self.file_name_label = QLabel('No File to display')

        close_btn = QPushButton(self)
        close_btn.setIcon(QIcon('assets/x.svg'))
        close_btn.setFixedWidth(button_width)
        close_btn.clicked.connect(self.close_current)

        # Tab which displays the file contents --------------------------------
        self.tab = QTabWidget(self)
        self.tab.setStyleSheet("QTabWidget::pane { padding: 0px; }")
        self.tab.tabBar().hide()

        placeholder = QLabel('Open a file or create a New one')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab.addTab(placeholder, 'placeholder')

        # Layout --------------------------------------------------------------
        layout = QGridLayout()
        self.setLayout(layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.tab)

        layout.addWidget(self.collapse_btn, 0, 0)
        layout.addWidget(file_btn, 0, 1)
        layout.addWidget(self.file_name_label, 0, 2)
        layout.addWidget(close_btn, 0, 3)
        layout.addWidget(splitter, 1, 0, 1, 4)
    
    def add_to_menu(self, name: str, menu: QMenu, trigger_func, shortcut: str=None):
        action = QAction(text=name, parent=self)
        action.triggered.connect(trigger_func)
        if shortcut:
            action.setShortcut(shortcut)
        menu.addAction(action)

    def toggle_file_browser_visible(self):
        visible = not self.tree.isVisible()
        self.tree.setVisible(visible)
        self.collapse_btn.setIcon(QIcon('assets/chevron-left.svg' if visible else 'assets/chevron-right.svg'))
        return visible
    
    def tree_item_clicked(self, item: TreeItem, _):
        self.switch(item)

    def open_file(self, file_path: str):
        adapter = self.file_handle.open(file_path, link_handle=self.open_file)
        self.mount(adapter, self.tree.currentItem())

    def open_menu(self):
        adapter = self.file_handle.open_dialog(self, link_handle=self.open_file)
        if adapter: self.mount(adapter)
    
    def mount(self, adapter: AA, parentItem: QTreeWidgetItem=None):
        if parentItem == None:
            parentItem = self.tree.invisibleRootItem()
        self.tab.addTab(adapter.get_widget(), "test")
        item = TreeItem(get_arr(adapter.get_file_path()), adapter, parentItem)
        parentItem.addChild(item)
        self.switch(item)
    
    def switch(self, item: TreeItem):
        self.tree.setCurrentItem(item)
        self.file_name_label.setText(item.adapter.get_basename())
        self.tab.setCurrentIndex(self.tab.indexOf(item.adapter.get_widget()))
    
    def close_current(self):
        item: TreeItem = self.tree.currentItem()
        if item:
            self.tab.removeTab(self.tab.indexOf(item.adapter.get_widget()))
            item.remove()
            item: TreeItem = self.tree.currentItem()
            if item:
                self.switch(item)
            else:
                self.file_name_label.setText('No File to display')

    def save(self):
        item: TreeItem = self.tree.currentItem()
        if item:
            file_path = self.file_handle.save(item.adapter)
            print(file_path)
            if file_path:
                f, e = get_arr(file_path)
                item.setText(0, f)
                item.setText(1, e)
                self.file_name_label.setText(os.path.basename(file_path))
    
    def save_as(self):
        item: TreeItem = self.tree.currentItem()
        if item:
            file_path = self.file_handle.save_as(item.adapter)
            print(file_path)
            if file_path:
                f, e = get_arr(file_path)
                item.setText(0, f)
                item.setText(1, e)
                self.file_name_label.setText(os.path.basename(file_path))

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import QRect
    import sys

    app = QApplication(sys.argv)
    noteApp = TreeTab()
    window = QMainWindow()
    window.setWindowTitle('PySideNote v0.1.0')
    window.setWindowIcon(QIcon('assets/Notes-Book--Streamline-Ultimate.svg'))
    window.setGeometry(QRect(100, 100, 800, 600))
    window.setCentralWidget(noteApp)

    window.show()
    app.exec()