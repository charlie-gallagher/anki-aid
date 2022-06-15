import forvo


params = {
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}

req_url = forvo.fv_build_pronounce_request(
        key = forvo.GLOBAL['API_KEY'],
        word = 'sledovat'
    )

audio = forvo.fv_get_audio_list(forvo.GLOBAL['API_KEY'], 'sledovat')

forvo.fv_get_czech_audio(
        key = forvo.GLOBAL['API_KEY'],
        wordlist = ['sledovat', 'naprosto', 'ahoj', 'this does not exist']
        )
