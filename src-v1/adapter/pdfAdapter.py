# adapter to view pdf documents such as e-books

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QTreeWidget,
    QTreeView,
    QSplitter,
)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfBookmarkModel, QPdfPageNavigator, QPdfDocument
from PySide6.QtCore import QUrl, QModelIndex, Qt

from abstractAdapter import AbstractAdapter as AA

class PdfAdapter(AA):
    def __init__(self, file_path):
        self.frame = QSplitter(Qt.Orientation.Horizontal)

        pdf_view = QPdfView()
        pdf_view.setPageMode(QPdfView.PageMode.MultiPage)

        self.bookmark_model = QPdfBookmarkModel(self.frame)
        pdf_doc = QPdfDocument()
        pdf_doc.load(file_path)
        pdf_view.setDocument(pdf_doc)
        self.bookmark_model.setDocument(pdf_view.document())

        bookmarks = QTreeView()
        bookmarks.setModel(self.bookmark_model)

        self.frame.addWidget(bookmarks)
        self.frame.addWidget(pdf_view)

        super().__init__()

    def navigate(self):
        print('here')

    def get_widget(self):
        return self.frame
    
# Adstract methods that need to return trivial values -------------------------
    def get_value(self):
        return ""
    
    def set_value(self, content):
        return
    
    def get_filter(self):
        return "PDF (*.pdf)"

# Concrete methods in AbstractAdapter that need to be overridden --------------
    def open(self, file_path):
        return
    
    def naive_save(self):
        return self.file_path
    
    def save_as(self):
        return self.file_path

if __name__ == "__main__":

    import widgetTester

    def create_widget():
        return PdfAdapter(
            'D:/programming/Python/PySide6 markdown note/content/pdf-example-bookmarks.pdf'
        ).get_widget()
    
    widgetTester.test('test pdf', create_widget)