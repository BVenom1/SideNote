from PySide6.QtWidgets import (
    QWidget,
    QFileDialog
)

from PySide6.QtCore import (
    QPersistentModelIndex
)

from abc import ABC, abstractmethod
import os

class AbstractAdapter(ABC):
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.open(self.file_path)
        self.tree_index = None
        self.tab_index = None
    
    def get_basename(self):
        return os.path.basename(self.file_path)

    @abstractmethod
    def get_value(self) -> str:
        pass

    @abstractmethod
    def set_value(self, content: str):
        pass

    @abstractmethod
    def get_widget(self) -> QWidget:
        pass

    @abstractmethod
    def get_filter(self) -> str:
        pass

    def set_persistent_indices(self, tree_index: QPersistentModelIndex, tab_index: QPersistentModelIndex):
        self.tree_index = tree_index
        self.tab_index = tab_index

    def open(self, file_path: str):
        if os.path.isfile(file_path):
            self.file_path = file_path
            with open(file_path, 'r') as file:
                self.set_value(file.read())

    def naive_save(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write(self.get_value())

    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self.get_widget(), "Save As", self.get_filter())
        if os.path.isfile(file_path):
            self.file_path = file_path
            self.naive_save()
    
    def save(self):
        if self.file_path != None:
            self.naive_save()
        else:
            self.save_as()

