# -*- coding: utf-8 -*-
__author__ = 'Messiah'
RUS = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENG = "abcdefghijklmnopqrstuvwxyz"
from re import search, sub, match, findall, MULTILINE, DOTALL

import requests


def caesar(encrypted):
    encrypted = unicode(encrypted).lower()
    if search(ur"[a-z]", encrypted):
        abc = ENG
    elif search(ur"[а-яё]", encrypted):
        abc = RUS
    else:
        return "", ""

    decrypted = []
    for rot in range(1, len(abc)):
        key = abc[rot:] + abc[:rot]
        trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
        decrypted.append(u"<tr><th>ROT{}</th><td>{}</td></tr>"
                         .format(rot, encrypted.translate(trans)))
    return (u"<abbr title=\"Cyclic shift\"><i class=\"icon-step-forward\"></i>"
            u" Caesar</abbr>",
            u"<table class=\"table-bordered table-stripped\">{}</table>"
            .format(u"".join(decrypted)))


def atbash(encrypted):
    encrypted = unicode(encrypted).lower()
    if search(ur"[a-z]", encrypted):
        abc = ENG
    elif search(ur"[а-яё]", encrypted):
        abc = RUS
    else:
        return "", ""
    key = abc[::-1]
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    return (u"<abbr title=\"A=Z B=Y...Y=B,Z=A\"><i class=\"icon-retweet\"></i>"
            u" Atbash</abbr>",
            u"<table class=\"table-bordered table-stripped\">{}</table>"
            .format(encrypted.translate(trans)))


def reverse(encrypted):
    return (u"<i class=\"icon-chevron-left\"></i>"
            u" Reversed text", encrypted[::-1])


def keymap(encrypted):
    encrypted = unicode(encrypted)
    key = (u"qwertyuiop[]asdfghjkl;'\<zxcvbnm,./`1234567890-="
           u"~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|>ZXCVBNM<>?")
    abc = (u"йцукенгшщзхъфывапролджэ\/ячсмитьбю.ё1234567890-="
           u"Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/|ЯЧСМИТЬБЮ,")
    if search(ur"[a-z]", encrypted):
        abc, key = key, abc
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    return (u"<i class=\"icon-globe\"></i>"
            u" Wrong Keymap", u"{}".format(encrypted.translate(trans)))


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

    encrypted = unicode(encrypted).split()

    def decode(text):
        result = []
        for c in text:
            try:
                result.append(letters[c])
            except KeyError:
                result.append(u"_")
        return u"".join(result)

    letters = signs
    letters.update(en)
    table = []
    result = decode(encrypted)
    if not match(ur"^_*$", result):
        table.append(u"<tr><th>ENG</th><td>{}</td></tr>"
                     .format(result))
    result = decode(" ".join(encrypted)
                    .translate({ord(u'.'): ord(u'-'),
                                ord(u'-'): ord(u'.')})
                    .split())
    if not match(ur"^_*$", result):
        table.append(u"<tr><th>ENG rev</th><td>{}</td></tr>"
                     .format(result))
    letters = signs
    letters.update(ru)
    result = decode(encrypted)
    if not match(ur"^_*$", result):
        table.append(u"<tr><th>RUS</th><td>{}</td></tr>"
                     .format(result))
    result = decode(" ".join(encrypted)
                    .translate({ord(u'.'): ord(u'-'),
                                ord(u'-'): ord(u'.')})
                    .split())
    if not match(ur"^_*$", result):
        table.append(u"<tr><th>RUS rev</th><td>{}</td></tr>"
                     .format(result))
    if len(table) > 0:
        return (u"<abbr>Morse</abbr>",
                u"<table class=\"table-bordered table-stripped\">{}</table>"
                .format(u"".join(table)))
    else:
        return "", ""


def from_hex(encrypted):
    try:
        return u"From HEX", u"".join(encrypted.split()).decode("hex")
    except ValueError:
        return "", ""


def from_ascii(encrypted):
    try:
        return u"From ASCII", u"".join([chr(int(i)) for i in encrypted.split()])
    except ValueError:
        return "", ""


def from_position(encrypted):
    try:
        positions = map(int, encrypted.split())
    except ValueError:
        return "", ""

    try:
        rus = map(lambda i: RUS[(i - 1) % 33], positions)
    except IndexError:
        rus = u""

    try:
        eng = map(lambda i: ENG[(i - 1) % 26], positions)
    except IndexError:
        eng = u""
    table = [u"<table class=\"table table-stripped\">"]
    if rus:
        table.append(u"<tr><th>RUS</th><td>{}</td></tr>".format("".join(rus)))
    if eng:
        table.append(u"<tr><th>ENG</th><td>{}</td></tr>".format("".join(eng)))
    table.append(u"</table>")
    if len(table) > 2:
        return u"From position", u"".join(table)
    else:
        return "", ""


def from_binary(encrypted):
    import binascii
    try:
        return (u"From BIN",
                binascii.unhexlify("%x" % int("0b{}".format(encrypted), 2)))
    except ValueError:
        return "", ""


def bacon(encrypted):
    """
    Bacon cipher (http://www.cs.ucf.edu/~gworley/files/baconian_cipher.txt)
    :param encrypted:
    """
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
    plaintext = u"".join(plaintext)
    if not match(ur"_*", plaintext):
        return u"<abbr title=\"AAABBBABAA\">Bacon</abbr>", plaintext
    else:
        return "", ""


def decapsulate(encrypted):
    """
    Decapsulate from text only:
        - english letters
        - russian letters
        - digits
        - english capital letters
        - russian capital letters
    :param encrypted:
    """
    table = [u"<table class=\"table table-bordered\">"]
    encrypted = unicode(encrypted)
    eng = findall("[A-Za-z]", encrypted)
    if len(eng) > 0:
        table.append(u"<tr><th>ENG letters:</th><td>{}</td></tr>"
                     .format(u" ".join(eng)))
    rus = findall(u"[а-яёФ-ЯЁ]", encrypted)
    if len(rus) > 0:
        table.append(u"<tr><th>RUS letters:</th><td>{}</td></tr>"
                     .format(u" ".join(rus)))
    enCap = findall("[A-Z]", encrypted)
    if len(enCap) > 0:
        table.append(u"<tr><th>EN Capital:</th><td>{}</td></tr>"
                     .format(u" ".join(enCap)))
    ruCap = findall(u"[А-ЯЁ]", encrypted)
    if len(ruCap) > 0:
        table.append(u"<tr><th>RUS Capital:</th><td>{}</td></tr>"
                     .format(u" ".join(ruCap)))
    digits = findall(u"[0-9]", encrypted)
    if len(digits) > 0:
        table.append(u"<tr><th>Digits:</th><td>{}</td></tr>"
                     .format(u" ".join(digits)))
    table.append(u"</table>")
    if len(table) > 2:
        return u"Decapsulated", u"".join(table)
    else:
        return "", ""


def anagram(encrypted):
    """
    Do the anagram search.
    Russian on 4maf.ru (thanks to authors)
    English on wordsmith.org (thanks, community!)
    :param encrypted:
    """
    encrypted = unicode(encrypted)
    if match(ur"[А-Яа-яёЁ]+", encrypted):
        payload = {
            "sourceword": encrypted,
            "ModType": 1,
            "minf": 0
        }
        try:
            r = requests.post("http://4maf.ru/anagram_ajax.php",
                              data=payload)
            return (u"Anagram",
                    r.text)
        except:
            pass
    elif match(r"[A-Za-z]+", encrypted):
        payload = {
            "anagram": encrypted,
            "t": 50,
            "a": "n"
        }
        try:
            r = requests.get("http://www.wordsmith.org/anagram/anagram.cgi",
                             params=payload)
            result = search(r"\d+ found\. Displaying all:\s*?</b>"
                            "<br>(.*?)<bottomlinks>",
                            r.text, MULTILINE | DOTALL)
            return u"Anagram", result.group(1)
        except:
            pass
    return "", ""


functions = [
    caesar,
    atbash,
    morse,
    from_hex,
    from_ascii,
    from_binary,
    from_position,
    bacon,
    keymap,
    reverse,
    decapsulate,
    anagram,
]


def main():
    pass


if __name__ == '__main__':
    main()
