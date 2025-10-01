from PySide6.QtWidgets import QWidget
import os
from abstractAdapter import AbstractAdapter

def fileSwitchOpen(file_path: str, **kwargs) -> AbstractAdapter:
    ext = os.path.splitext(file_path)[1]
    print(f"opening {file_path}, ext: f{ext}")
    if ext == '.md':
        from markdownAdapter import MarkdownAdapter
        link_handle = kwargs['link_handle'] if 'link_handle' in kwargs else None
        return MarkdownAdapter(file_path, link_handle)
    elif ext == '.txt':
        from textAdapter import TextAdapter
        return TextAdapter(file_path)
