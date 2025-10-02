import os
from abstractAdapter import AbstractAdapter

def file_switch_open(file_path: str, **kwargs) -> AbstractAdapter:
    split = os.path.splitext(file_path)
    ext = split[1] if split[1] != '' else split[0]
    print(f"opening {file_path}, ext: {ext}")
    if ext == '.md':
        from markdownAdapter import MarkdownAdapter
        link_handle = kwargs['link_handle'] if 'link_handle' in kwargs else None
        return MarkdownAdapter(file_path, link_handle)
    elif ext == '.txt':
        from textAdapter import TextAdapter
        return TextAdapter(file_path)
