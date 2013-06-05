# -*- coding: utf-8 -*-
__author__ = 'Messiah'
RUS = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENG = "abcdefghijklmnopqrstuvwxyz"
from re import search, sub
from string import maketrans


def caesar(encrypted):
    encrypted = u"{}".format(encrypted).lower()
    if search(r"[a-z]", encrypted):
        abc = ENG
    else:
        abc = RUS

    decrypted = []
    for rot in range(1, len(abc)):
        key = abc[rot:] + abc[:rot]
        trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
        decrypted.append(u"<tr><th>ROT{}</th><td>{}</td></tr>"
                         .format(rot, encrypted.translate(trans)))
    return ("Caesar",
            u"<table class=\"table-bordered table-stripped\">{}</table>"
            .format("".join(decrypted)))


def atbash(encrypted):
    encrypted = u"{}".format(encrypted).lower()
    if search(r"[a-z]", encrypted):
        abc = ENG
    else:
        abc = RUS
    key = abc[::-1]
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    return (u"Substitution A=Z B=Y ...",
            u"<table class=\"table-bordered table-stripped\">{}</table>"
            .format(encrypted.translate(trans)))


def reverse(encrypted):
    return u"Reversed text", encrypted[::-1]


def keymap(encrypted):
    encrypted = u"{}".format(encrypted)
    key = (u"qwertyuiop[]asdfghjkl;'\<zxcvbnm,./`1234567890-="
           u"~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|>ZXCVBNM<>?")
    abc = (u"йцукенгшщзхъфывапролджэ\/ячсмитьбю.ё1234567890-="
           u"Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/|ЯЧСМИТЬБЮ,")
    if search(r"[a-z]", encrypted):
        abc, key = key, abc
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    return "Wrong Keymap", u"{}".format(encrypted.translate(trans))


def morse(encrypted):
    signs = {u'.....': u'5', u'-.--.-': u'(', u'..--..': u'?', u'.----': u'1',
             u'---...': u':', u'......': u'.', u'----.': u'9', u'---..': u'8',
             u'..---': u'2', u'-.-.--': u'!', u'....-': u'4', u'-....': u'6',
             u'-.-.-.': u';', u'-----': u'0', u'-.-.-.-': u',', u'...--': u'3',
             u'.-..-.': u"'", u'--...': u'7', u'/': u' ', u'--..--': u','}

    en = {u'---': u'O', u'--.': u'G', u'-...': u'B', u'-..-': u'X',
          u'.-.': u'R', u'--.-': u'Q', u'--..': u'Z', u'.--': u'W',
          u'.-': u'A', u'..': u'I', u'-.-.': u'C', u'..-.': u'F',
          u'-.--': u'Y', u'-': u'T', u'.': u'E', u'.-..': u'L', u'...': u'S',
          u'..-': u'U', u'-.-': u'K', u'-..': u'D', u'.---': u'J',
          u'.--.': u'P', u'--': u'M', u'-.': u'N', u'....': u'H',
          u'...-': u'V'}

    ru = {u"..-..": u'Э',  u"---": u'О',  u"--.": u'Г',  u"-...": u'Б',
          u"-..-": u'Ь',  u".-.": u'Р',  u"--.-": u'Ы',  u"--..": u'З',
          u".--": u'В',  u".-": u'А',  u"..": u'И',  u"-.-.": u'Ц',
          u"..-.": u'Ф',  u"..--": u'Ю',  u"-": u'Т',  u".": u'Е',
          u".-.-": u'Я',  u".-..": u'Л',  u"--.--": u'Ъ',  u"...": u'С',
          u"..-": u'У',  u"----": u'Ш',  u"---.": u'Ч',  u"-.-": u'К',
          u"-..": u'Д',  u".---": u'Й',  u".--.": u'П',  u"--": u'М',
          u"-.": u'Н',  u"....": u'Х',  u"...-": u'Ж'}

    encrypted = u"{}".format(encrypted).split()

    def decode(input):
        result = []
        for c in input:
            try:
                result.append(letters[c])
            except KeyError:
                result.append(u"_")
        return u"".join(result)

    letters = signs
    letters.update(en)
    table = []
    table.append(u"<tr><th>ENG</th><td>{}</td></tr>".format(
        decode(encrypted)))
    table.append(u"<tr><th>ENG rev</th><td>{}</td></tr>".format(
        decode(" ".join(encrypted).translate({ord(u'.'): ord(u'-'),
                                              ord(u'-'): ord(u'.')}).split())))
    letters = signs
    letters.update(ru)
    table.append(u"<tr><th>RUS</th><td>{}</td></tr>".format(
        decode(encrypted)))
    table.append(u"<tr><th>RUS rev</th><td>{}</td></tr>".format(
        decode(" ".join(encrypted).translate({ord(u'.'): ord(u'-'),
                                              ord(u'-'): ord(u'.')}).split())))
    return ("Morse",
            u"<table class=\"table-bordered table-stripped\">{}</table>"
            .format("".join(table)))


def from_hex(encrypted):
    return "From HEX", u"".join(encrypted.split()).decode("hex")


def from_ascii(encrypted):
    return "From ASCII", u"".join([chr(int(i)) for i in encrypted.split()])


def from_binary(encrypted):
    import binascii
    return ("From BIN",
            binascii.unhexlify("%x" % int("0b{}".format(encrypted), 2)))


def bacon(encrypted):
    bacondict = {}
    plaintext = []

    encrypted = encrypted.lower()
    encrypted = sub("[\W\d]", "", encrypted.strip())
    for i in range(26):
        tmp = bin(i)[2:].zfill(5)
        tmp = tmp.replace('0', 'a')
        tmp = tmp.replace('1', 'b')
        bacondict[tmp] = chr(65 + i)

    for i in range(len(encrypted) / 5):
        plaintext.append(bacondict.get(encrypted[i * 5:i * 5 + 5], '_'))
    return "Bacon", u"".join(plaintext)

functions = [
    caesar,
    atbash,
    morse,
    from_hex,
    from_ascii,
    from_binary,
    bacon,
    keymap,
    reverse,
]


def main():
    pass


if __name__ == '__main__':
    main()
