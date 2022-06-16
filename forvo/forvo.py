# Query data from Forvo
import os
import requests
import urllib
import pathlib
# This non-sense because I haven't figured out how to get
# from anki_cli import cli
# to work
import sys
sys.path.append('anki_cli')
import cli

def fv_get_api_key(file):
    with open(file, 'r') as f:
        key = f.readline().rstrip()
    
    return key


GLOBAL = {
    'API_KEY': fv_get_api_key(os.path.expanduser('~/forvo-key.txt'))
}



def fv_path_param(params):
    """
    Converts parameter dictionary to the format required by the Forvo
    API, which looks like this:

    ```
    key1/value1/key2/value2
    ```

    Which I know is ugly as hell. Anyway.
    """
    if type(params) is not dict:
        raise TypeError
    
    key_combos = [x + '/' + y for x,y in zip(params.keys(), params.values())]

    return '/'.join(key_combos)




def fv_build_pronounce_request(key, word, language = 'cs', order = 'rate-desc', **args):
    url = 'https://apifree.forvo.com'
    params = fv_path_param({
        'key': key,
        'action': 'word-pronunciations',
        'format': 'json',
        'word': word,
        'language': language,
        'order': order,
        **args
    })

    url_params = urllib.parse.quote(params)
    url_combined = url + '/' + url_params

    return url_combined


def fv_get_audio_list(key, word):
    """
    Get list of Audio files from the Forvo API converted from JSON.
    """
    url = fv_build_pronounce_request(key = key, word = word)

    r = requests.get(url = url)
    r.raise_for_status()

    return r.json()


def fv_retrieve_audio(url, path):
    """
    Download MP3 from the temporary URL returned by the API.

    url: URL of the MP3
    path: Path to write
    """
    mp3 = requests.get(url)
    mp3.raise_for_status()

    # Pretty printing stuff
    print(cli.check(f'Writing to {cli.blue(str(path))}'))

    # Write to disk
    with open(path, 'wb') as f:
        f.write(mp3.content)

    return path


def fv_filter_czech_audio_list(resp, preferred_users):
    """
    Attempt to filter the MP3 response to preferred users 

    resp: content of the audio API response
    preferred_users: List, usernames of preferred users on Forvo

    Returns a string -- the MP3 URL of the first preferred user found --
    or None if no users are present.
    """
    return None


def fv_get_czech_audio(key, wordlist, audio_dir = 'mp3', preferred_users = ['Zababa', 'Mili_CZ']):
    """
    Search and download Czech audio files from Forvo

    Searches Forvo for a word and downloads the "best" recording, by the
    following list of priority:

    1. Preferred users, as defined by `fv_filter_czech_audio_list`
    2. Highest rated recording

    Returns a list of successful words
    """
    successes = list()
    for word in wordlist:
        print(f'Searching Forvo for {cli.blue(word)}')
        audio = fv_get_audio_list(key = key, word = word)
        print(f'Found {cli.blue(str(len(audio["items"])))} recordings')

        if (len(audio['items']) == 0):
            print('No recordings found!')
            continue

        # Take the first MP3
        mp3 = audio['items'][0]['pathmp3']

        # If priority returns anything, overwrite mp3 with the priority
        priority_mp3 = fv_filter_czech_audio_list(audio, preferred_users)
        if priority_mp3 is not None:
            mp3 = priority_mp3

        print('Downloading audio...')
        fv_retrieve_audio(mp3, pathlib.Path(audio_dir, f'pronunciation_cs_{word}.mp3'))
        successes.append(word)
        

    print(f'Successfully found {cli.blue(str(len(successes)))} words')
    return wordlist
