from random import randrange, choice
from string import ascii_letters, digits, punctuation

def get_charlist(use_punctuation = True):
    charlist = ascii_letters + digits
    if use_punctuation: charlist = charlist + punctuation
    charlist = charlist.replace('\"','')
    charlist = charlist.replace('\'','')
    charlist = charlist.replace(',','')
    return charlist

def random_character():
    """generates a random character from character list"""
    charlist = get_charlist()
    randomchar = choice(charlist)
    return randomchar

def random_sequence(lower_bound = 12, upper_bound = 17):
    """creates string of random characters"""
    length = randrange(lower_bound, upper_bound)
    sequence = ''.join([random_character() for _ in range(length)])
    return sequence
