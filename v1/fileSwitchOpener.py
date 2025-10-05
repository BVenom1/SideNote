import os
from adapter.abstractAdapter import AbstractAdapter
from PySide6.QtWidgets import QFileDialog

def file_switch_open(file_path: str, **kwargs) -> AbstractAdapter:
    split = os.path.splitext(file_path)
    ext = split[1] if split[1] != '' else split[0]
    # print(f"opening {file_path}, ext: {ext}")
    if ext == '.md':
        from adapter.markdownAdapter import MarkdownAdapter
        link_handle = kwargs['link_handle'] if 'link_handle' in kwargs else None
        return MarkdownAdapter(file_path, link_handle)
    elif ext == '.txt':
        from adapter.textAdapter import TextAdapter
        return TextAdapter(file_path)


class FileHandler():
    def __init__(self):
        return
    
    def open(self, file_path: str, **kwargs) -> AbstractAdapter:
        content = ''
        if os.path.isfile(file_path):
            self.file_path = file_path
            with open(file_path, 'r') as file:
                content = file.read()
        else:
            file_path = f'untitled{file_path}'
        split = os.path.splitext(file_path)
        ext = split[1] if split[1] != '' else split[0]
        if ext == '.md':
            from adapter.markdownAdapter import MarkdownAdapter
            link_handle = kwargs['link_handle'] if 'link_handle' in kwargs else None
            return MarkdownAdapter(content, file_path, link_handle)
        elif ext == '.txt':
            from adapter.textAdapter import TextAdapter
            return TextAdapter(content, file_path)
        
    def naive_save(self, adapter: AbstractAdapter) -> str:
        with open(adapter.get_file_path(), 'w') as file:
            file.write(adapter.get_value())
        return adapter.file_path
    
    def save_as(self, adapter: AbstractAdapter) -> str:
        file_path, _ = QFileDialog.getSaveFileName(adapter.get_widget(), "Save As", filter=adapter.get_filter())
        if file_path:
            adapter.set_file_path(file_path)
            return self.naive_save(adapter)
        else:
            return None
    
    def save(self, adapter: AbstractAdapter):
        return self.naive_save(adapter) if os.path.isfile(adapter.get_file_path()) else self.save_as(adapter)