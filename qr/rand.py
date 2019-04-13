"""A Layer for google authenticator style login suite
"""
from random import SystemRandom
import string


def make_pseudo_word(syllables=5, add_number=False):
    """Create decent memorable passwords.

    Alternate random consonants & vowels
    """
    rnd = SystemRandom()
    s = string.ascii_lowercase
    vowels = 'aeiou'
    consonants = ''.join([x for x in s if x not in vowels])
    pwd = ''.join([rnd.choice(consonants) + rnd.choice(vowels) for x in range(syllables)])
    if add_number:
        pwd += str(rnd.choice(range(10)))
    return pwd


def rand_str(count=10):
    """Generate a random string...
    """
    choice = SystemRandom().choice
    ls=string.ascii_letters
    return ''.join(choice(ls) for x in range(count))


def gen_16():
    """Generate a new secret work of 16
    """
    a = make_pseudo_word(4, True)
    #print(len(a), a)
    b = make_pseudo_word(4, False)

    return (a+b)[:16]


