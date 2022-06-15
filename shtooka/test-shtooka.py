import shtooka as shtk
import json
import os

index_exists = os.path.exists('data/index.json')

# If the index does not exist, generate it
if not index_exists:
    # The indices are stored at these URIs
    ivana_url = "https://packs.shtooka.net/ces-balm-ivana/mp3/index.xml"
    veronika_url = "https://packs.shtooka.net/ces-balm-veronika/mp3/index.xml"
    nums_url = "https://packs.shtooka.net/ces-balm-veronika-num/mp3/index.xml"

    # build_shtooka_index combines all three indices into one
    # usable dictionary
    index_urls = [ivana_url, veronika_url, nums_url]
    index = shtk.build_shtooka_index(index_urls)

    with open('data/index.json', 'w') as f:
        f.write(json.dumps(index))
else:
    print("Found cached index!")
    print("To use a different index, delete the 'data/index.json' file")




# Read index, wordlist, and search for words
with open('data/index.json', 'r') as f:
    index = json.load(f)

with open('data/wordlist.txt', 'r') as f:
    wordlist = [x.rstrip() for x in f]


total_status = list()
for word in wordlist:
    status = shtk.sh_get_audio(word, index)
    total_status.append(status)

print(total_status)

