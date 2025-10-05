from PySide6.QtWidgets import (
    QWidget,
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

