from PySide6.QtCore import (
    QRegularExpression,
)
from PySide6.QtGui import (
    QSyntaxHighlighter,
    QTextDocument,
    QTextCharFormat,
    QColor,
    QTextBlockFormat,
    QTextListFormat,
    QTextCursor,
)

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument):
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
            (QRegularExpression(r"\*([^*]+)\*"), italic_format),
            (QRegularExpression(r"\*\*([^*]+)\*\*"), bold_format),
            (QRegularExpression(r"_([^*]+)_"), italic_format),
            (QRegularExpression(r"__([^*]+)__"), bold_format),
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