from PySide6.QtWidgets import (
    QFrame,
    QTextBrowser,
    QPushButton,
    QGridLayout,
)
from PySide6.QtGui import (
    QIcon,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextBlockFormat,
    QTextListFormat,
    QColor,
    QTextDocument,
    QTextCursor,
)
from PySide6.QtCore import QRegularExpression, Qt, QUrl

import os

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument, foo_func):
        super().__init__(parent)
        
        header_format = QTextCharFormat()
        header_format.setFontWeight(800)
        header_format.setFontPointSize(18)
        
        subheader_format = QTextCharFormat()
        subheader_format.setFontWeight(800)
        subheader_format.setFontPointSize(13.5)
        
        inline_code_format = QTextCharFormat()
        inline_code_format.setBackground(QColor("#68826f"))
        
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(800)
        
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        
        quote_format = QTextBlockFormat()
        quote_format.setBackground(QColor("#68826f"))
        quote_format.setLeftMargin(40)
        
        bullet_list_format = QTextListFormat()
        bullet_list_format.setStyle(QTextListFormat.Style.ListDisc)
        
        self.char_formats = [
            (QRegularExpression(r"^#\s.*$"), header_format),
            (QRegularExpression(r"^##\s.*$"), subheader_format),
            (QRegularExpression(r"`([^`]+)`"), inline_code_format),
            (QRegularExpression(r"\*([^*]+)\*"), bold_format),
            (QRegularExpression(r"_([^*]+)_"), italic_format),
        ]
        
        self.block_formats = [
            (QRegularExpression(r"^>\s.*$"), quote_format),
        ]
        
        self.list_formats = [
            (QRegularExpression(r"^(\s*)[*+-]\s+.*$"), bullet_list_format),
        ]
        
        self.update_fonts = [
            (header_format, 4),
            (subheader_format, 3),
        ]
    
    def get_update_fonts(self):
        return self.update_fonts
        
    def highlightBlock(self, text):
        cursor = QTextCursor(self.document())
        cursor.setPosition(self.currentBlock().position())
        for pattern, format in self.block_formats:
            match = pattern.match(text)
            if match.hasMatch():
                cursor.setBlockFormat(format)
                break
        
        for pattern, format in self.list_formats:
            match = pattern.match(text)
            if match.hasMatch():
                cursor.createList(format)
                break
        
        for pattern, format in self.char_formats:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class Adapter(QFrame):
    def __init__(self, content: str = '', file_path: str = None):
        super().__init__()
        
        self.is_editable = True
        
        self.staged_hashtag_replace = False
        
        self.text = QTextBrowser()
        self.text.setReadOnly(False)
        self.text.setOpenLinks(False)
        self.text.cursorPositionChanged.connect(self.text_changed)
        self.text.anchorClicked.connect(self.anchor_clicked)
        self.highlighter = Highlighter(self.text.document(), lambda x: print(x))
        
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
    
    def text_changed(self):
        self.text.blockSignals(True)
        # remove the link of current word
        cursor = self.text.textCursor()
        while True:
            cursor.movePosition(
                QTextCursor.MoveOperation.PreviousCharacter,
                QTextCursor.MoveMode.KeepAnchor
            )
            t = cursor.selectedText()
            if t == '' or t[0] == ' ' or not cursor.position():
                break
        cursor.clearSelection()
        while True:
            cursor.movePosition(
                QTextCursor.MoveOperation.PreviousCharacter,
                QTextCursor.MoveMode.KeepAnchor
            )
            t = cursor.selectedText()
            if t == '' or t[0] == ' ' or not cursor.position():
                break
        pos = cursor.position()
        regex = QRegularExpression(r"#[A-Za-z0-9_\-]+")
        match = regex.match(cursor.selectedText())
        if match.hasCaptured(0):
            start = pos + match.capturedStart(0)
            length = match.capturedLength(0)
            cursor.setPosition(start, QTextCursor.MoveMode.MoveAnchor)
            cursor.setPosition(start + length, QTextCursor.MoveMode.KeepAnchor)
            t = cursor.selectedText()
            cursor.removeSelectedText()
            cursor.insertHtml(f"<a href='{t}'>{t}</a>")
        self.text.blockSignals(False)
    
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
        self.text.setMarkdown(content)

if __name__ == '__main__':
    
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import QRect
    import sys
    
    app = QApplication(sys.argv)
    
    # content = ''
    # file_path = "D:/Notes/PySideNote Notes/Sanskrit nouns.md"
    # with open(file_path, 'r', encoding='utf8') as file:
    #     content = file.read()
    
    noteApp = Adapter()
    window = QMainWindow()
    window.setWindowTitle('PySideNote v0.1.0')
    window.setWindowIcon(QIcon('assets/Notes-Book--Streamline-Ultimate.svg'))
    window.setGeometry(QRect(100, 100, 800, 600))
    window.setCentralWidget(noteApp)

    window.show()
    app.exec()