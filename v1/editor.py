from PySide6.QtWidgets import (
    QFrame,
    QTextBrowser,
    QPushButton,
    QGridLayout,
)
from PySide6.QtGui import (
    QIcon,
    QTextCursor,
)
from PySide6.QtCore import Qt, QUrl, QRegularExpression

import os

from highlighter import Highlighter
from textBrowser import TextBrowser

class Editor(QFrame):
    def __init__(self, content: str = '', file_path: str = None):
        super().__init__()
        
        self.is_editable = True
        
        self.staged_hashtag_replace = False
        
        self.text = TextBrowser(parent=self, link_handle=self.anchor_clicked)
        self.highlighter = Highlighter(self.text.document())
        
        zoom_in_btn = QPushButton(parent=self)
        zoom_in_btn.setIcon(QIcon('assets/zoom-in.svg'))
        zoom_in_btn.clicked.connect(self.zoom_in)
        
        zoom_out_btn = QPushButton(parent=self)
        zoom_out_btn.setIcon(QIcon('assets/zoom-out.svg'))
        zoom_out_btn.clicked.connect(self.zoom_out)
        
        btn = QPushButton('foo', parent=self)
        btn.clicked.connect(self.foo)
        
        btn2 = QPushButton('bar', parent=self)
        btn2.clicked.connect(self.bar)
        
        btn3 = QPushButton('foobar', parent=self)
        btn3.clicked.connect(lambda: print(self.text.toHtml()))
        
        layout = QGridLayout()
        layout.setColumnStretch(2, 1)
        
        layout.addWidget(zoom_in_btn, 0, 0)
        layout.addWidget(zoom_out_btn, 0, 1)
        layout.addWidget(btn, 0, 2)
        layout.addWidget(btn2, 0, 3)
        layout.addWidget(btn3, 0, 4)
        layout.addWidget(self.text, 1, 0, 1, 5)
        
        self.setLayout(layout)
        
        self.set_value(content)
        self.set_file_path(file_path)
    
    def anchor_clicked(self, link: QUrl):
        print(link.toString())
    
    def foo(self):
        cursor = self.text.textCursor()
        fragment = cursor.selectedText()
        cursor.removeSelectedText()
        cursor.insertHtml(f"<a href='{fragment}'>{fragment}</a>")
        print(fragment)
        
    def bar(self):
        if self.is_editable:
            self.text.setTextInteractionFlags(
                Qt.TextInteractionFlag.LinksAccessibleByMouse |
                Qt.TextInteractionFlag.TextBrowserInteraction
            )
        else:
            self.text.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextEditorInteraction
            )
        self.is_editable = not self.is_editable
    
    def zoom_in(self):
        font = self.text.font()
        point_size = font.pointSize() + 2
        font.setPointSize(point_size)
        self.text.setFont(font)
        for format, size in self.highlighter.get_update_fonts():
            format.setFontPointSize(format.fontPointSize() + size)
        self.highlighter.rehighlight()
        
    def zoom_out(self):
        font = self.text.font()
        point_size = font.pointSize()
        if point_size > 9: point_size -= 2
        else: return
        font.setPointSize(point_size)
        self.text.setFont(font)
        for format, size in self.highlighter.get_update_fonts():
            format.setFontPointSize(format.fontPointSize() - size)
        self.highlighter.rehighlight()

    def set_file_path(self, file_path: str):
        self.file_path = file_path
    
    def get_file_path(self) -> str:
        return self.file_path
    
    def get_basename(self):
        return os.path.basename(self.file_path)

    def get_value(self) -> str:
        return self.text.toPlainText()

    def set_value(self, content: str):
        self.text.setPlainText(content)

if __name__ == '__main__':
    
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import QRect
    import sys
    
    app = QApplication(sys.argv)
    
    content = ''
    file_path = "D:/programming/Python/PySide6 markdown note/content/text_example.txt"
    with open(file_path, 'r', encoding='utf8') as file:
        content = file.read()
    
    noteApp = Editor(content, file_path)
    window = QMainWindow()
    window.setWindowTitle('PySideNote v0.1.0')
    window.setWindowIcon(QIcon('assets/Notes-Book--Streamline-Ultimate.svg'))
    window.setGeometry(QRect(100, 100, 800, 600))
    window.setCentralWidget(noteApp)

    window.show()
    app.exec()