# coding: utf-8
import os
import json
import re

document_sections = [
    'violence_tags',
    'document_title',
    'document_text',
    'search_tags'
]

document_sections_abbr = [
    'violence_tags',
    'document_text',
    'search_tags'
]


def remove_blank_str(string):
    return (string != '') & (string is not None)


def clean_tag(tag):
    tag_clean = ' '.join(filter(remove_blank_str, tag.lower().strip().split()))
    tag_clean = ' '.join(filter(remove_blank_str, tag_clean.split('.')))
    return tag_clean


def parse_tags(contents, tag_name):

    tags_raw = contents.get(tag_name, '')
    # Split tags sections into individual tags
    tags = re.split('\n|\r|,', tags_raw)

    # Clean individual tags
    tags = filter(remove_blank_str, [clean_tag(tag) for tag in tags])

    return tags


def parse_file_contents(file_raw):

    # Split file by deliminter and store as dict
    file_contents = file_raw.split('***')
    if len(file_contents) == 3:
        contents = dict(zip(document_sections_abbr, file_contents))
    elif len(file_contents) == 4:
        contents = dict(zip(document_sections, file_contents))
    elif len(file_contents) > 4:
        raise ValueError(
            'Document has too many sections: ' + str(len(file_contents)))
    else:
        raise ValueError(
            'Document has too few sections: ' + str(len(file_contents)))

    # Split tags sections into individual tags
    contents['violence_tags'] = parse_tags(contents, 'violence_tags')
    contents['search_tags'] = parse_tags(contents, 'search_tags')

    # Return dictionary of cleaned file contents
    return contents


def parse_files(dirname, verbose=False):

    docs_clean = {}
    for filename in os.listdir(dirname):
        # Read through all txt files in specified directory
        if filename.endswith(".txt"):
            if verbose:
                print "Reading {}".format(filename)
            with open(os.path.join(dirname, filename)) as f:
                file_raw = f.read()
                try:
                    doc_clean = parse_file_contents(file_raw)
                except ValueError as error:
                    print 'File: ' + str(filename)
                    print repr(error)
                except UnicodeDecodeError as err:
                    print repr(err)
                docs_clean[filename] = doc_clean

    print "Read {} files from directory {}".format(len(docs_clean), dirname)
    return docs_clean

if __name__ == "__main__":
    docs_clean = parse_files("documents")
    with open('docs_clean.json', 'w') as f:
        json.dump(docs_clean, f)
