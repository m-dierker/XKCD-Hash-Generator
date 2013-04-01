import urllib.request, urllib.parse, urllib.error
import random
from skein import skein1024
import os

diff_table = {}

def main():
    min_bits = 405
    xkcd_hash = "5b4da95f5fa08280fc9879df44f418c8f9f12ba424b7757de02bbdfbae0d4c4fdf9317c80cc5fe04c6429073466cf29706b8c25999ddd2f6540d4475cc977b87f4757be023f19b8f4035d7722886b78869826de916a79cf9c94cc79cd4347d24b567aa3e2390a573a373a48a5e676640c79cc70197e1c5e7f902fb53ca1858b6"

    # Generate diff table
    for a in range(16):
        diff_table[a] = {}
        for b in range(16):
            c = a ^ b
            diff = 0
            while c != 0:
                if c % 2 == 1:
                    diff += 1
                c = c >> 1
            diff_table[a][b] = diff

    word = str(os.getpid() + random.randint(0, 100000))
    word = hashWord(word)

    count = 0

    while True:
        count += 1
        if count % 100000 == 0:
            print(count)

        word_hash = hashWord(word)
        diff = hash_diff(word_hash, xkcd_hash)
        if (diff < min_bits):
            min_bits = diff
            print("Found a new word \"" + word + "\" that only differs by " + str(diff) + " bits")
            sendWord(word)

        word = word_hash

def hashWord(word):
    """ Returns a hash for a given word """
    h = skein1024(word.encode('UTF-8'), digest_bits=1024)
    return h.hexdigest()

def hash_diff(hash1, hash2):
    """ Returns the difference between two hashes """
    diff = 0
    for x in range(256):
        diff += diff_table[int(hash1[x], 16)][int(hash2[x], 16)]
    return diff


def sendWord(word):
    """ Returns the number of bits the word is off by """
    data = 'hashable=' + word
    url = urllib.request.urlopen('http://almamater.xkcd.com/?edu=uiuc.edu', data.encode('UTF-8'))
    url.close()

if __name__ == '__main__':
    main()
