from audiocz import cli
from audiocz import copy_to_anki
from audiocz import forvo

if __name__ == "__main__":
    with open('data/wordlist.txt', 'r') as f:
        wordlist = [x.rstrip() for x in f]

    print(cli.h1('Searching Forvo'))
    wordlist = forvo.ForvoWordlist(
            wordlist = wordlist,
            api_key_file = '~/forvo-key.txt',
            download_dir = 'mp3'
        )
    wordlist.search()
    wordlist.download()
    wordlist.format_anki_references()
    copy_to_anki.cp_copy_new_mp3s(
        audio_dir='mp3',
        anki_dir='mp3/fake_anki'
    )

