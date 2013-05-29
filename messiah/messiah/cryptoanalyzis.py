# -*- coding: utf-8 -*-
__author__ = 'Messiah'
RUS = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENG = "abcdefghijklmnopqrstuvwxyz"
from re import search

def caesar(encrypted):
    encrypted = u"{}".format(encrypted).lower()
    if search(r"[a-z]", encrypted):
        abc = ENG
    else:
        abc = RUS
        
    decrypted = []
    for rot in range(len(abc)):
        key = abc[rot:] + abc[:rot]
        trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
        decrypted.append(u"<tr><th>ROT{}</th><td>{}</td></tr>"
                         .format(rot, encrypted.translate(trans)))
    return "Caesar", u"<table>{}</table>".format("".join(decrypted))


functions = [
    caesar,
]


def main():
    pass


if __name__ == '__main__':
    main()
