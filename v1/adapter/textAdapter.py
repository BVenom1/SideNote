from adapter.abstractAdapter import AbstractAdapter as AA

from PySide6.QtWidgets import (
    QTabWidget,
    QTextEdit
)

class TextAdapter(AA):
    def __init__(self,content='', file_path=None):
        self.text_area = QTextEdit()
        super().__init__(content, file_path)
    
# Implementations of abstract methods in AbstractAdapter ----------------------
    def get_value(self):
        return self.text_area.toPlainText()
    
    def set_value(self, content):
        self.text_area.setPlainText(content)
    
    def get_widget(self):
        return self.text_area
    
    def get_filter(self):
        return "Text (*.txt)"