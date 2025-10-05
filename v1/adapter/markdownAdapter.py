from PySide6.QtWidgets import (
    QTextEdit,
    QSplitter,
    QTextBrowser,
    QFrame,
    QGridLayout,
    QPushButton,
)

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon

from adapter.abstractAdapter import AbstractAdapter as AA
import os

import re

class MarkdownAdapter(AA):
    def __init__(self, content='', file_path=None, link_handle=None):
        self.link_handle = link_handle

        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame { padding: 0px; margin: 0px; }")
        view = QSplitter(Qt.Orientation.Horizontal)

        self.text = QTextEdit(view)
        view.addWidget(self.text)
        self.text.textChanged.connect(self.convert_to_markdown)

        self.browser = QTextBrowser(view)
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(lambda link: self.handle_link(link))
        view.addWidget(self.browser)
        
        text_zoom_in_btn = QPushButton(parent=self.frame)
        text_zoom_in_btn.setIcon(QIcon('assets/zoom-in.svg'))
        text_zoom_in_btn.clicked.connect(lambda: self.zoom_in(self.text))
        
        text_zoom_out_btn = QPushButton(parent=self.frame)
        text_zoom_out_btn.setIcon(QIcon('assets/zoom-out.svg'))
        text_zoom_out_btn.clicked.connect(lambda: self.zoom_out(self.text))
        
        browser_zoom_in_btn = QPushButton(parent=self.frame)
        browser_zoom_in_btn.setIcon(QIcon('assets/zoom-in.svg'))
        browser_zoom_in_btn.clicked.connect(lambda: self.zoom_in(self.browser))
        
        browser_zoom_out_btn = QPushButton(parent=self.frame)
        browser_zoom_out_btn.setIcon(QIcon('assets/zoom-out.svg'))
        browser_zoom_out_btn.clicked.connect(lambda: self.zoom_out(self.browser))
        
        layout = QGridLayout(self.frame)
        self.frame.setLayout(layout)
        
        layout.setColumnStretch(2, 1)
        
        layout.addWidget(text_zoom_in_btn, 0, 0)
        layout.addWidget(text_zoom_out_btn, 0, 1)
        layout.addWidget(browser_zoom_in_btn, 0, 3)
        layout.addWidget(browser_zoom_out_btn, 0, 4)
        
        layout.addWidget(view, 1, 0, 1, 5)
        
        super().__init__(content, file_path)
        
    def zoom_in(self, text: QTextEdit):
        font = text.font()
        font.setPointSize(font.pointSize() + 2)
        text.setFont(font)
    
    def zoom_out(self, text: QTextEdit):
        font = text.font()
        if font.pointSize() > 9:
            font.setPointSize(font.pointSize() - 2)
            text.setFont(font)
    
    def handle_link(self, link: QUrl):
        if link.scheme() == "":
            self.browser.scrollToAnchor(link.fragment())
        else:
            file_path = link.toString()
            if self.link_handle: self.link_handle(file_path)
    
    def convert_to_markdown(self):
        self.browser.setMarkdown(self.text.toPlainText())
    
    def get_links(self):
        i_list = re.findall(r"\[.*\]\(.*\)", self.text.toPlainText())
        def process(l: str):
            i = re.search(r'\(<.*>\)', l)
            if i:
                return i.group()[2:-2]
            return re.search(r'\(.*\)', l).group()[1:-1]
        f_list = map(process, i_list)
        return f_list
    
# Implementations of abstract methods in AbstractAdapter ----------------------
    def get_value(self):
        for i in self.get_links():
            print(i)
            print(os.path.isfile(i))
        return self.text.toPlainText()
    
    def set_value(self, content):
        self.text.setPlainText(content)
    
    def get_widget(self):
        return self.frame
    
    def get_filter(self):
        return "Markdown (*.md)"