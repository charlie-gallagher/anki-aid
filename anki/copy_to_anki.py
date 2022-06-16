# Utilities for copying files to Anki `collection.media` directory
# I'm not sure how I'll incorporate the (system-dependent) Anki
# media directory
import os
import shutil
from pathlib import Path
import sys
# This non-sense because I haven't figured out how to get
# from anki_cli import cli
# to work
sys.path.append('anki_cli')
import cli

GLOBALS = {'audio_dir': 'mp3', 'anki_dir': 'mp3/fake_anki'}

ANKI_DIR = Path(
    os.path.expanduser('~'),
    'Library',
    'Application Support',
    'Anki2',
    'User 1',
    'collection.media'
)

# Take all of the files in `audio_dir` and copy them 
# into `anki_dir`. Don't copy files that exist in the
# target location. Report which files will be copied
# and their copy status.

# There's a warning on shutil that not all attributes are
# copied, such as the file owner and group. I'll do some
# experiments.

def cp_get_new_mp3_names(audio_dir, anki_dir):
    """
    Find MP3 files in audio_dir that are not in anki_dir
    """
    audio_dir = Path(audio_dir)
    anki_dir = Path(anki_dir)

    anki_mp3s = [p.name for p in anki_dir.glob('*.mp3')]
    audio_mp3s = [p.name for p in audio_dir.glob('*.mp3')]

    return list(set(audio_mp3s).difference(anki_mp3s))


def cp_copy_new_mp3s(audio_dir, anki_dir):
    """
    Copy mp3 files to the Anki dir
    """
    new_mp3s = cp_get_new_mp3_names(audio_dir, anki_dir)

    from_mp3s = [Path(audio_dir, x) for x in new_mp3s]
    to_dir = Path(anki_dir)

    for x in from_mp3s:
        shutil.copy(x, to_dir)
        msg = f'Writing {cli.blue(str(x))} to Anki directory'
        print(f'{cli.check(msg)}')

    msg = f'Successfully copied {cli.blue(str(len(new_mp3s)))} files to Anki'
    print(cli.check(msg))
    return new_mp3s

