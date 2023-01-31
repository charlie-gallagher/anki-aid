from pydub import AudioSegment, effects
if __name__=='__main__':
    import cli
else:
    from . import cli

def normalize(file):
    print(cli.check(f'Normalizing {cli.blue(file)}'))
    raw_sound = AudioSegment.from_file(file, 'mp3')
    normalized_sound = effects.normalize(raw_sound)
    normalized_sound.export(file, format='mp3')


