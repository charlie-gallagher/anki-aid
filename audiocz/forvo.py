# Query data from Forvo
import os
import requests
import urllib
import pathlib
# Enable testing using main function
if __name__=='__main__':
    import cli
    from wordlist import Wordlist
# Otherwise just use relative import
else:
    from . import cli
    from .wordlist import Wordlist


def get_api_key(api_key_file):
    with open(os.path.expanduser(api_key_file), 'r') as f:
        key = f.readline().rstrip()
    return key


class ForvoRequest:
    def __init__(self, key_file, word):
        self.key = get_api_key(key_file)
        self.word = word

    def build_pronounce_request(self, language = 'cs', order = 'rate-desc', **args):
        url = 'https://apifree.forvo.com'
        params = params_to_path({
            'key': self.key,
            'action': 'word-pronunciations',
            'format': 'json',
            'word': self.word,
            'language': language,
            'order': order,
            **args
        })
        url_params = urllib.parse.quote(params)
        url_combined = url + '/' + url_params
        return url_combined


    def get_audio_list(self):
        """
        Get list of Audio files from the Forvo API converted from JSON.
        """
        url = self.build_pronounce_request()
        r = requests.get(url = url)
        r.raise_for_status()
        return r.json()


def params_to_path(params):
    """
    Converts parameter dictionary to the format required by the Forvo
    API, which looks like this:

        key1/value1/key2/value2
    """
    if type(params) is not dict:
        raise TypeError
    key_combos = [x + '/' + y for x,y in zip(params.keys(), params.values())]
    return '/'.join(key_combos)


class ForvoResponseItem:
    def __init__(self, resp_item):
        try:
            self.id = resp_item['id']
            self.word = resp_item['word']
            self.username = resp_item['username']
            self.url = resp_item['pathmp3']
            self.upvotes = resp_item['num_positive_votes']
            self.downvotes = resp_item['num_votes'] - resp_item['num_positive_votes']
        except KeyError:
            print("Malformed response")
            raise


class ForvoResponse:
    """A ForvoResponse object

    Pass in a word and its API response and you can download the word, filter
    for certain users, and generate an Anki media reference.

    @param word The word used to search for the audio files
    @param resp The API response containing the audio files
    """
    def __init__(self, word, resp):
        self.n_results = None
        self.word = word
        self.responses = []
        self._parse_resp(word=word, resp=resp)

    def _parse_resp(self, word, resp):
        self.n_results = resp['attributes']['total']
        for x in resp['items']:
            self.responses.append(ForvoResponseItem(x))

    def filter_by_username(self, users):
        return [x for x in self.responses if x.username in users]

    def download(self, target_dir = '.', priority_users = ('Mili_CZ', 'Zababa')):
        user_sublist = self.filter_by_username(priority_users)
        if len(user_sublist) != 0:
            url = self._choose_url(user_sublist)
        else:
            url = self._choose_url(self.responses)
        target_path = make_filename(target_dir, self.word)
        return self._download_item(url, target_path)

    @staticmethod
    def _choose_url(responses):
        max_votes = max([x.upvotes for x in responses])
        to_download = [x.url for x in responses if x.upvotes == max_votes]
        # This allows ties -- in that case, take the first recording
        return to_download[0]

    @staticmethod
    def _download_item(url, path):
        mp3 = requests.get(url)
        mp3.raise_for_status()
        print(cli.check(f'Writing to {cli.blue(str(path))}'))
        with open(path, 'wb') as f:
            f.write(mp3.content)
        return path

    def format_anki_reference(self):
        return f'[sound:pronunciation_cs_{self.word.replace(" ", "_")}.mp3]'


def make_filename(path, word):
    word_clean = word.replace(' ', '_')
    word_filename = f'pronunciation_cs_{word_clean}.mp3'
    return pathlib.PurePath(path, word_filename)


class ForvoWordlist(Wordlist):
    """A Wordlist subclass with methods for searching Forvo

    @param wordlist An iterable containing the words to search for
    @param api_key_file The file that contains the API key
    @param download_dir The directory into which files get downloaded
    """
    def __init__(self, wordlist, api_key_file, download_dir):
        self.wordlist = wordlist
        self.download_dir = download_dir
        self.successes = []
        self.failures = []

        # Forvo-specific fields
        self.api_key_file = api_key_file
        self.api_key = get_api_key(api_key_file)

    def search(self):
        self.responses = self._search_forvo()
        self.successes = [x for x in self.responses if x.n_results > 0]
        self.failures = [x for x in self.responses if x.n_results == 0]
        self.summarize_responses()

    def _search_forvo(self):
        out = []
        for word in self.wordlist:
            print(f'Searching for {cli.blue(word)}...', end='', flush=True)
            fv = ForvoRequest(key_file=self.api_key_file, word=word)
            resp = ForvoResponse(word=word, resp=fv.get_audio_list())
            out.append(resp)
            print('Done')
        return out

    def summarize_responses(self):
        print(cli.h1('Successful searches'))
        if len(self.successes) == 0:
            print(cli.fail('No successful searches'))
        else:
            for word_resp in self.successes:
                print(cli.check(word_resp.word))
        print(cli.h1('Failed searches'))
        if len(self.failures) == 0:
            print(cli.fail('No failed searches'))
        else:
            for word_resp in self.failures:
                print(cli.fail(word_resp.word))

    def download(self):
        print(cli.h1('Starting downloads'))
        for resp in self.successes:
            # This already does pretty printing
            resp.download(self.download_dir)

    def format_anki_references(self):
        for resp in self.successes:
            print(resp.format_anki_reference())




if __name__=='__main__':
    print("Object creation works")
    key_file = "~/forvo-key.txt"
    fv = ForvoRequest(key_file = key_file, word = 'dobrý')
    
    print("Read API key")
    print(fv.key)

    print("Test out getter")
    res = fv.get_audio_list()
    print(res)

    print("Test ForvoResponse")
    fv_res = ForvoResponse(word='dobrý', resp=res)
    print(fv_res)
    print(f'Length: {fv_res.n_results}')
    print("Find username")
    print(fv_res.filter_by_username(('kunk', 'Mili_CZ')))
    print(fv_res.filter_by_username('not a username'))

    print("Download test")
    fv_res.download('./mp3')

    print("Formatted for anki")
    print(fv_res.format_anki_reference())

    print("A whole wordlist")
    words = [
                'dobrý',
                'den',
                'jak',
                'se',
                'máš',
            ]

    print("Create wordlist")
    wordlist = ForvoWordlist(
            wordlist = words,
            api_key_file = '~/forvo-key.txt',
            download_dir = 'mp3'
        )
    print("Get results")
    wordlist.search()
    print("Download results")
    wordlist.download()
    wordlist.format_anki_reference()


