from PySide6.QtWidgets import (
    QSplitter,
    QTextEdit,
)
from PySide6.QtCore import (
    Qt,
    QUrl,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

from abstractAdapter import AbstractAdapter as AA

class WebPage(QWebEnginePage):
    def __init__(self, link_handle):
        super().__init__()
        self.link_handle = link_handle

    def acceptNavigationRequest(self, url: QUrl, type, isMainFrame):
        if type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            self.link_handle(url)
            return False
        return False

class HtmlAdapter(AA):
    def __init__(self, file_path=None, link_handle=None):
        self.view = QSplitter(Qt.Orientation.Horizontal)

        self.text = QTextEdit(self.view)
        self.view.addWidget(self.text)
        self.text.textChanged.connect(self.convert_to_html)

        self.browser = QWebEngineView(self.view)
        page = WebPage(self.handle_link)
        self.browser.setPage(page)
        self.view.addWidget(self.browser)

        super().__init__(file_path)

    def handle_link(self, link: QUrl):
        print(link)
    
    def convert_to_html(self):
        self.browser.setHtml(self.text.toPlainText())
    
    def get_value(self):
        return self.text.toPlainText()
    
    def set_value(self, content):
        self.text.setPlainText(content)
    
    def get_widget(self):
        return self.view

    def get_filter(self):
        return 'HTML (*.html)'