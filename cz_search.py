from audiocz import cli
from audiocz import copy_to_anki
from audiocz import forvo
from audiocz import shtooka


if __name__ == "__main__":
    with open('data/wordlist.txt', 'r') as f:
        wordlist = [x.rstrip() for x in f]

    print(cli.h1('Searching Forvo'))
    forvo.fv_get_czech_audio(key = forvo.GLOBAL['API_KEY'], wordlist = wordlist)
