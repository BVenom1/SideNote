from abstractAdapter import AbstractAdapter as AA

from PySide6.QtWidgets import (
    QTabWidget,
    QTextEdit
)

class TextAdapter(AA):
    def __init__(self, file_path=None):
        self.text_area = QTextEdit()
        super().__init__(file_path)
    
    def get_value(self):
        return self.text_area.toPlainText()
    
    def set_value(self, content):
        self.text_area.setPlainText(content)
    
    def get_widget(self):
        return self.text_area
    
    def get_filter(self):
        return "Text (*.txt)"

if __name__ == "__main__":
    
    import widgetTester
    
    def close_tab(tab: QTabWidget):
        tab.removeTab(tab.currentIndex())

    def create_tab():
        tab = QTabWidget()
        tab.setTabsClosable(True)
        tab.tabCloseRequested.connect(lambda: close_tab(tab))
        adapter = TextAdapter(tab, "D:/programming/Python/PySide6 markdown note/content/text_example.txt")
        tab.addTab(adapter.get_widget(), "untitled.txt")
        return tab
    widgetTester.test("TextAdapter", create_tab)