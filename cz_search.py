from audiocz import cli
from audiocz import copy_to_anki
from audiocz import forvo
# from audiocz import shtooka

# def shtooka_init():
#     index_exists = os.path.exists('data/index.json')
# 
#     # If the index does not exist, generate it
#     if not index_exists:
#         # The indices are stored at these URIs
#         ivana_url = "https://packs.shtooka.net/ces-balm-ivana/mp3/index.xml"
#         veronika_url = "https://packs.shtooka.net/ces-balm-veronika/mp3/index.xml"
#         nums_url = "https://packs.shtooka.net/ces-balm-veronika-num/mp3/index.xml"
# 
#         # build_shtooka_index combines all three indices into one
#         # usable dictionary
#         index_urls = [ivana_url, veronika_url, nums_url]
#         index = shtk.build_shtooka_index(index_urls)
# 
#         with open('data/index.json', 'w') as f:
#             f.write(json.dumps(index))
#     else:
#         print("Found cached index!")
#         print("To use a different index, delete the 'data/index.json' file")
# 
# 
# def shtooka_search_all(wordlist, index_path):
#     # Read index, wordlist, and search for words
#     with open(index_path, 'r') as f:
#         index = json.load(f)
# 
#     success_words = list()
#     for word in wordlist:
#         status = shtk.sh_get_audio(word, index)
#         if (status is True):
#             success_words.append(word)
# 
#     return success_words
# 
# 
# def success_summary(wordlist, success_words, origin):
#     """
#     Print a summary of a word get attempt
# 
#     wordlist: List of words attempted
#     success_words: List of words successfully gotten
#     origin: String, the name of the attempter (e.g., Shtooka)
#     """
#     print(cli.h1(f'{origin} summary'))
#     for word in success_words:
#         print(cli.check(word))
#     failed_words = list(set(wordlist).difference(success_words))
#     for word in failed_words:
#         print(cli.fail(word))




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
    wordlist.
    copy_to_anki.cp_copy_new_mp3s(
        audio_dir='mp3',
        anki_dir='mp3/fake_anki'
    )

