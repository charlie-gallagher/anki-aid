# Download Audio for Anki Flashcards
Downloading audio for Anki language flashcards is a pain, but easy to automate.
This is a Python-based assistant for downloading audio files from Forvo and
Shtooka (when it's available), and moving them to the Anki media directory.

It's still under-developed -- I really haven't gotten this working yet.
Actually, I have an R-based version that I use more regularly, but this will
have more features and a better implementation, I think.

Currently only works for Czech.

It's also not a package yet. In fact, just don't use this.

## Setup
Install the requirements.

```
pip3 install -r requirements.txt
```

## audiocz
The primary module is `audiocz`, which contains sub-modules:

- `cli` Tools for writing to stdout in a pretty way
- `copy_to_anki` Tools for writing to the Anki media directory
- `forvo` (recently superseded by `forvo_class`) Tools for downloading from
  Forvo
- `shtooka` same as `forvo` but for `shtooka.org`
- and `wordlist`, which contains an empty abstract `Wordlist` class that I'll
  flesh out at some point.


## Example
Download files from Forvo with something like the following:

```py
words = [
            'dobrý',
            'den',
            'jak',
            'se',
            'máš',
        ]

wordlist = ForvoWordlist(
        wordlist = words,
        # NOTE: Update to match a text file containing your forvo key
        api_key_file = '~/forvo-key.txt',
        # NOTE: Update to match where you want the files to end up
        download_dir = './mp3'
    )

wordlist.search_forvo()
wordlist.download()
```

---

Charlie Gallagher, January 2023
