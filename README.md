# Download Audio for Anki Flashcards
Downloading audio for Anki language flashcards is a pain, but easy to automate.
This is a Python-based assistant for downloading audio files from Forvo and
Shtooka (when it's available), and moving them to the Anki media directory.

Currently only works for Czech.

It's also not a package yet. In fact, just don't use this, but feel free to use
it.

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

NOTE: Shtooka lately has been letting its SSL certificate lapse, so I don't
recommend using it anymore. It's too unreliable. (It's a shame, though, because
the recordings are pristine.)
If you want, you can download the wordlists locally and rename the files using
the XML data dictionaries.


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

wordlist.search()
wordlist.download()
wordlist.format_anki_references()
```

Once you have the files downloaded locally, you can copy them to the Anki shared
media directory. This could also be done during the download step if you like.
The `copy_to_anki` module will check for duplicate files and only copy those to
Anki that are not already there.

---

Charlie Gallagher, January 2023
