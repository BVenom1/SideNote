from adapter.abstractAdapter import AbstractAdapter as AA

from PySide6.QtWidgets import (
    QTextEdit,
    QFrame,
    QPushButton,
    QGridLayout,
)

from PySide6.QtGui import QIcon

class TextAdapter(AA):
    def __init__(self,content='', file_path=None):
        
        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame { padding: 0px; margin: 0px; }")
        self.text_area = QTextEdit()
        
        zoom_in_btn = QPushButton(parent=self.frame)
        zoom_in_btn.setIcon(QIcon('assets/zoom-in.svg'))
        zoom_in_btn.clicked.connect(self.zoom_in)
        
        zoom_out_btn = QPushButton(parent=self.frame)
        zoom_out_btn.setIcon(QIcon('assets/zoom-out.svg'))
        zoom_out_btn.clicked.connect(self.zoom_out)
        
        layout = QGridLayout(self.frame)
        self.frame.setLayout(layout)
        layout.setColumnStretch(0, 1)
        layout.addWidget(zoom_in_btn, 0, 1)
        layout.addWidget(zoom_out_btn, 0, 2)
        layout.addWidget(self.text_area, 1, 0, 1, 3)
        
        super().__init__(content, file_path)
    
    def zoom_in(self):
        font = self.text_area.font()
        font.setPointSize(font.pointSize() + 2)
        self.text_area.setFont(font)
    
    def zoom_out(self):
        font = self.text_area.font()
        if font.pointSize() > 9:
            font.setPointSize(font.pointSize() - 2)
            self.text_area.setFont(font)
    
# Implementations of abstract methods in AbstractAdapter ----------------------
    def get_value(self):
        return self.text_area.toPlainText()
    
    def set_value(self, content):
        self.text_area.setPlainText(content)
    
    def get_widget(self):
        return self.frame
    
    def get_filter(self):
        return "Text (*.txt)"