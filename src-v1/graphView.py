from tinydb import TinyDB, Query
import os
import json

from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
)
from PySide6.QtCore import (
    QObject,
    Slot,
    QUrl,
)

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel

db_src = 'D:/programming/Python/PySide6 markdown note/src-v1/data/test.json'

# add test data to the database
def add_data():
    db = TinyDB(db_src)
    db.truncate()   # clear the database

    nodes = db.table('nodes')
    nodes.truncate()

    x = nodes.insert_multiple([
        {
            'name': 'save-txt',
            'type': 'TXT',
            'path': 'D:/programming/Python/PySide6 markdown note/content/save-txt.txt'
        },
        {
            'name': 'tab-save',
            'type': 'MD',
            'path': 'D:/programming/Python/PySide6 markdown note/content/tab-save.md'
        },
    ])

    links = db.table('links')
    links.truncate()

    links.insert_multiple([
        {
            'source': 'D:/programming/Python/PySide6 markdown note/content/save-txt.txt',
            'target': 'D:/programming/Python/PySide6 markdown note/content/tab-save.md'
        }
    ])

    # print(nodes.all())
    # print(links.all())
# add_data()

class CallHandler(QObject):

    def __init__(self, sup):
        super().__init__()
        self.sup = sup
        self.db = TinyDB(db_src)
        self.nodes = self.db.table('nodes')
        self.links = self.db.table('links')
    
    # @Slot(str)
    # def get_links(self, *args):
    #     print(args[0])

    @Slot(result=str)
    def get_nodes(self):
        return json.dumps(self.nodes.all())
    
    @Slot(result=str)
    def get_links(self):
        return json.dumps(self.links.all())



class WebView(QWebEngineView):
    def __init__(self):
        super().__init__()

        self.channel = QWebChannel()
        self.handler = CallHandler(self)
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)

        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "data/view.html"
            )
        )
        local_url = QUrl.fromLocalFile(file_path)

        self.load(local_url)

class GraphView(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # button = QPushButton("Open", self)
        # layout.addWidget(button)

        self.web_view = WebView()
        layout.addWidget(self.web_view)


if __name__ == "__main__":

    import widgetTester

    def create_widget():
        return GraphView()

    widgetTester.test('test', create_widget)

