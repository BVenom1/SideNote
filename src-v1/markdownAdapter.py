from PySide6.QtWidgets import (
    QTabWidget,
    QTextEdit,
    QSplitter,
    QTextBrowser,
)

from PySide6.QtCore import Qt, QUrl

from abstractAdapter import AbstractAdapter as AA

class MarkdownAdapter(AA):
    def __init__(self, parent: QTabWidget, file_path: str = None):
        self.view = QSplitter(Qt.Orientation.Horizontal)

        self.text = QTextEdit(parent)
        self.view.addWidget(self.text)
        self.text.textChanged.connect(self.convert_to_markdown)

        self.browser = QTextBrowser(parent)
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(lambda link: self.handle_link(link))
        self.view.addWidget(self.browser)
        
        super().__init__(parent, file_path)

    
    def handle_link(self, link: QUrl):
        if link.scheme() == "":
            self.browser.scrollToAnchor(link.fragment())
        else:
            file_path = link.toString()
            print(file_path)
            from fileSwitchOpener import fileSwitchOpen
            new_adapter = fileSwitchOpen(self.p, file_path)
            self.p.addTab(new_adapter.get_widget(), new_adapter.get_basename())
    
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