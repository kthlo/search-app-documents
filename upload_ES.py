import os
import warnings
from elasticsearch import Elasticsearch, RequestsHttpConnection
import parse_documents as parse


class ES_uploader:

    def __init__(self):
        self.index_nm = 'nssd'
        self.docs_clean = parse.parse_files("documents")
        self.es = Elasticsearch(
            hosts=os.environ['ES_HOST'],
            verify_certs=True,
            connection_class=RequestsHttpConnection)

    def rm_create_index(self):
        es = self.es
        es.indices.delete(index=self.index_nm, ignore=[400, 404])
        es.indices.create(index=self.index_nm)['acknowledged']

    def index_doc(self, doc):
        _id = doc[0]
        d = doc[1]
        status = self.es.index(index='nssd', doc_type='doc', body=d, id=_id)
        if not status['created']:
            warnings('Document {} not created'.format(status['_id']))

    def index_all_docs(self):
        for doc in self.docs_clean.items():
            self.index_doc(doc)

if __name__ == '__main__':
    uploader = ES_uploader()
    uploader.rm_create_index()
    uploader.index_all_docs()
