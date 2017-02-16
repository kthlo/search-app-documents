import parse_documents as parse
import random
from collections import defaultdict
import config


class Document_explorer():
    def __init__(self):
        # Parse documents
        self.docs_clean = parse.parse_files(config.path_documents)

    def find_docs_by_tag(self, tag, tag_type):
        """Get list of documents containing violence tag
        """
        match_docs = []
        for key, value in self.docs_clean.iteritems():
            v_tags = value[tag_type]
            for v_tag in v_tags:
                if v_tag == tag:
                    match_docs.append(key)
        return match_docs

    def get_unique_tags(self, tag_type):
        """Get unique violence tags
        """
        tags = defaultdict(int)
        for key, value in self.docs_clean.iteritems():
            v_tags = value[tag_type]
            for v_tag in v_tags:
                tags[v_tag] += 1
        return tags

    def print_tags(self, i):
        print '{}: {}'.format(i, self.docs_clean.items()[i][0])
        print self.docs_clean.items()[i][1]['violence_tags']
        print self.docs_clean.items()[i][1]['search_tags']

    def print_random_tags(self):
        self.print_tags(random.randrange(0, len(self.docs_clean)))

if __name__ == '__main__':
    d = Document_explorer()

    # Print unique violence tags
    violence_tags = d.get_unique_tags('violence_tags')
    print('{} unique violence tags found:'.format(len(violence_tags)))
    for v, i in violence_tags.items():
        print('   {}: {}'.format(v, i))

    # Print unique search tags
    search_tags = d.get_unique_tags('search_tags')
    print('\n{} unique search tags found:'.format(len(search_tags)))
    for v, i in search_tags.items():
        print('   {}: {}'.format(v, i))
