from PySide6.QtWidgets import (
    QTabWidget,
    QTextEdit,
    QSplitter,
    QTextBrowser,
)

from PySide6.QtCore import Qt, QUrl

from abstractAdapter import AbstractAdapter as AA

class MarkdownAdapter(AA):
    def __init__(self, file_path=None, link_handle=None):
        self.link_handle = link_handle

        self.view = QSplitter(Qt.Orientation.Horizontal)

        self.text = QTextEdit(self.view)
        self.view.addWidget(self.text)
        self.text.textChanged.connect(self.convert_to_markdown)

        self.browser = QTextBrowser(self.view)
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(lambda link: self.handle_link(link))
        self.view.addWidget(self.browser)
        
        super().__init__(file_path)
    
    def handle_link(self, link: QUrl):
        if link.scheme() == "":
            self.browser.scrollToAnchor(link.fragment())
        else:
            file_path = link.toString()
            if self.link_handle: self.link_handle(file_path)
    
    def convert_to_markdown(self):
        self.browser.setMarkdown(self.text.toPlainText())
    
    def get_value(self):
        return self.text.toPlainText()
    
    def set_value(self, content):
        self.text.setPlainText(content)
    
    def get_widget(self):
        return self.view
    
    def get_filter(self):
        return "Markdown (*.md)"

if __name__ == "__main__":
    
    import widgetTester
    
    def close_tab(tab: QTabWidget):
        tab.removeTab(tab.currentIndex())

    def create_tab():
        tab = QTabWidget()
        tab.setTabsClosable(True)
        tab.tabCloseRequested.connect(lambda: close_tab(tab))
        adapter = MarkdownAdapter(tab, "D:/programming/Python/PySide6 markdown note/content/test-link.md")
        tab.addTab(adapter.get_widget(), adapter.get_basename())
        return tab
    widgetTester.test("TextAdapter", create_tab)