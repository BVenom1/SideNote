from PySide6.QtWidgets import (
    QTabWidget,
    QTextEdit,
    QSplitter,
    QTextBrowser,
)

from PySide6.QtCore import Qt, QUrl

from adapter.abstractAdapter import AbstractAdapter as AA
import os

import re

class MarkdownAdapter(AA):
    def __init__(self, content='', file_path=None, link_handle=None):
        self.link_handle = link_handle

        self.view = QSplitter(Qt.Orientation.Horizontal)

        self.text = QTextEdit(self.view)
        self.view.addWidget(self.text)
        self.text.textChanged.connect(self.convert_to_markdown)

        self.browser = QTextBrowser(self.view)
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(lambda link: self.handle_link(link))
        self.view.addWidget(self.browser)
        
        super().__init__(content, file_path)
    
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
        return self.view
    
    def get_filter(self):
        return "Markdown (*.md)"