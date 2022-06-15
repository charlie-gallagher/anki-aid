# Utilities for querying the Shtooka files

# Index files:
# "https://packs.shtooka.net/ces-balm-ivana/mp3/index.xml"
# "https://packs.shtooka.net/ces-balm-veronika/mp3/index.xml"
# "https://packs.shtooka.net/ces-balm-veronika-num/mp3/index.xml"
import requests
import xml.etree.ElementTree as ET
import pathlib

def get_raw_shtooka_xml(url):
    r = requests.get(url)
    return r.text

def read_raw_shtooka_xml(text):
    root = ET.fromstring(text)
    return root

def extract_shtooka_paths(shtooka_xml):
    filepaths = shtooka_xml.findall('.//file/[@path]')
    text_nodes = shtooka_xml.findall('.//file/tag/[@swac_text]')
    pack_loc = shtooka_xml.find('group').get('swac_coll_url')

    index = dict()
    for fp,word in zip(filepaths, text_nodes):
        p_text = fp.get('path')
        p_text_with_path = pack_loc + 'mp3/' + p_text
        word_text = word.get('swac_text')
        index[word_text] = p_text_with_path

    return index


def build_shtooka_index(urls):
    """
    Build the Shtooka index dictionary

    Returns a dictionary where the keys are Czech words and the
    values are URIs for the mp3 files.

    This is the highest level function.

    Audio files for the same words are given precedence in the 
    order they are given.
    """
    d_list = list()
    # Generate list of dictionaries
    for url in urls:
        print("Fetching index at " + url + "...")
        xml_raw = get_raw_shtooka_xml(url)
        xml_proc = read_raw_shtooka_xml(xml_raw)
        d_list.append(extract_shtooka_paths(xml_proc))

    print("Done!")
    # Combine list of dictionaries
    index = dict()
    for d in d_list:
        index.update(d)

    return index


def sh_get_audio(word, lookup, path = 'mp3'):
    """
    Download a word from Shtooka

    Returns a logical indicating whether the file was
    successfully found and downloaded.

    word: a string, the word to look for
    lookup: A dictionary of shtooka indices
    path: Directory in which to write the file (the 
          filename is automatically generated)
    """
    if not word in lookup:
        print(f'❌ {word} not found on Shtooka')
        return False

    url = lookup[word]
    r = requests.get(url)
    r.raise_for_status()

    filename = sh_make_filename(path, word)
    print("✅ Writing " + str(filename))

    with open(filename, 'wb') as f:
        f.write(r.content)

    return True


def sh_make_filename(path, word):
    word_clean = word.replace(' ', '_')
    word_filename = f'pronunciation_cs_{word_clean}.mp3'
    return pathlib.PurePath(path, word_filename)
     




