from PySide6.QtWidgets import (
    QWidget,
    QFileDialog
)

from abc import ABC, abstractmethod
import os

class AbstractAdapter(ABC):
    def __init__(self, content: str = '', file_path: str = None):
        self.set_value(content)
        self.file_path = file_path

    def set_file_path(self, file_path: str):
        self.file_path = file_path
    
    def get_file_path(self) -> str:
        return self.file_path
    
    def get_basename(self):
        return os.path.basename(self.file_path)

# Abstract methods, to be provided implementations in child classes -----------
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

    # def open(self, file_path: str):
    #     if os.path.isfile(file_path):
    #         self.file_path = file_path
    #         with open(file_path, 'r') as file:
    #             self.set_value(file.read())
    #     else:
    #         self.file_path = f'untitled{file_path}'

    # def naive_save(self):
    #     with open(self.file_path, 'w') as file:
    #         file.write(self.get_value())
    #     return self.file_path

    # def save_as(self):
    #     file_path, _ = QFileDialog.getSaveFileName(self.get_widget(), "Save As", filter=self.get_filter())
    #     if file_path:
    #         self.file_path = file_path
    #         return self.naive_save()
    #     else:
    #         return None
    
    # def save(self):
    #     return self.naive_save() if os.path.isfile(self.file_path) else self.save_as()

