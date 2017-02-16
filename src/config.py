from os import path

path_src = path.abspath(path.dirname(__file__))
path_base = path.dirname(path_src)
path_data = path.join(path_base, 'data')
path_documents = path.join(path_base, 'documents')
