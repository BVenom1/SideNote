from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QMenu,
    QToolButton,
)

from PySide6.QtGui import (
    QIcon,
    QAction
)

from treeTab import TreeTab

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        self.tab = TreeTab(self)
        self.setCentralWidget(self.tab)

        self.collapse_btn = QAction(text='Collapse', parent=self)
        self.collapse_btn.setIcon(QIcon('assets/chevron-up.svg'))
        self.collapse_btn.triggered.connect(self.collapse_file_browser)
        toolbar.addAction(self.collapse_btn)

        file_menu = QMenu('File', self)
        file_btn = QToolButton(self)
        file_btn.setIcon(QIcon('assets/menu.svg'))
        file_btn.setMenu(file_menu)
        file_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        file_btn.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        toolbar.addWidget(file_btn)

        self.add_to_menu('Open', file_menu, self.tab.open_menu, 'Ctrl+O')
        self.add_to_menu('New Markdown', file_menu, lambda: self.tab.mount('.md'), 'Ctrl+M')
        self.add_to_menu('New Text', file_menu, lambda: self.tab.mount('.txt'), 'Ctrl+T')
        self.add_to_menu('Save', file_menu, self.tab.save, 'Ctrl+S')
        self.add_to_menu('Save As', file_menu, self.tab.save_as, 'Ctrl+A')

        close_btn = QAction(text='Close', parent=self)
        close_btn.setIcon(QIcon('assets/x.svg'))
        close_btn.triggered.connect(self.tab.close_current)
        toolbar.addAction(close_btn)
    
    def collapse_file_browser(self):
        visible = self.tab.toggle_file_browser_visible()
        self.collapse_btn.setIcon(
            QIcon('assets/chevron-up.svg' if visible else 'assets/chevron-down.svg')
        )

    def add_to_menu(self, name: str, menu: QMenu, trigger_func, shortcut: str=None):
        action = QAction(text=name, parent=self)
        action.triggered.connect(trigger_func)
        if shortcut:
            action.setShortcut(shortcut)
        menu.addAction(action)
    
if __name__ == "__main__":
    import widgetTester

    def create_tree_tab():
        return Window()
    
    widgetTester.test('test tree tabs mounting', create_tree_tab)