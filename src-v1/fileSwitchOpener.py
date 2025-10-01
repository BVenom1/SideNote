from PySide6.QtWidgets import QWidget
import os
from abstractAdapter import AbstractAdapter

def fileSwitchOpen(parent: QWidget, file_path: str) -> AbstractAdapter:
    ext = os.path.splitext(file_path)[1]
    print(f"opening {file_path}, ext: f{ext}")
    if ext == '.md':
        from markdownAdapter import MarkdownAdapter
        return MarkdownAdapter(parent, file_path)
    elif ext == '.txt':
        from textAdapter import TextAdapter
        return TextAdapter(parent, file_path)
