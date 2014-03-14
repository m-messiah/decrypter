# -*- coding: utf-8 -*-
__author__ = 'm_messiah'
RUS = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENG = "abcdefghijklmnopqrstuvwxyz"
BACONDICT = {}
for letter_counter in range(26):
    tmp = bin(letter_counter)[2:].zfill(5)
    tmp = tmp.replace('0', 'a')
    tmp = tmp.replace('1', 'b')
    BACONDICT[tmp] = chr(65 + letter_counter)

dictionary = [set(map(lambda x: x.decode("utf-8").rstrip(),
                  open("decrypter/words/en.txt").readlines())),
              set(map(lambda x: x.decode("utf-8").rstrip(),
                  open("decrypter/words/ru.txt").readlines()))]

phonepad = [[
    [u" "],
    [u""],               [u"a", u"b", u"c"],    [u"d", u"e", u"f"],
    [u"g", u"h", u"i"],  [u"j", u"k", u"l"],    [u"m", u"n", u"o"],
    [u"p", u"q", u"r", u"s"], [u"t", u"u", u"v"], [u"w", u"x", u"y", u"z"]
],
    [
    [u" "], [u""],
    [u"а", u"б", u"в", u"г"], [u"д", u"е", u"ж", u"з"],
    [u"и", u"й", u"к", u"л"], [u"м", u"н", u"о", u"п"],
    [u"р", u"с", u"т", u"у"], [u"ф", u"х", u"ц", u"ч"],
    [u"ш", u"щ", u"ъ", u"ы"], [u"ь", u"э", u"ю", u"я"]
    ]
]

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


from re import search, sub, match, findall, MULTILINE, DOTALL
import requests
import itertools


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
        decrypted.append(u"<div class=\"pure-u-1-3\"><p>ROT{}</p></div>"
                         .format(rot))
        decrypted.append(u"<div class=\"pure-u-2-3\"><p>{}</p></div>"
                         .format(encrypted.translate(trans)))
    return (u"<abbr title=\"Cyclic shift\">Caesar</abbr>",
            u"<div class=\"pure-g\">{}</div>".format(u"".join(decrypted)))


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
    return (u"<abbr title=\"A=Z B=Y...Y=B,Z=A\">Atbash</abbr>",
            u"{}".format(encrypted.translate(trans)))


def reverse(encrypted):
    return u" Reversed text", encrypted[::-1]


def keymap(encrypted):
    encrypted = unicode(encrypted)
    key = (u"qwertyuiop[]asdfghjkl;'\<zxcvbnm,./`1234567890-="
           u"~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|>ZXCVBNM<>?")
    abc = (u"йцукенгшщзхъфывапролджэ\/ячсмитьбю.ё1234567890-="
           u"Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/|ЯЧСМИТЬБЮ,")
    if search(ur"[a-z]", encrypted):
        abc, key = key, abc
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    return u" Wrong Keymap", u"{}".format(encrypted.translate(trans))


def morse(encrypted):
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
    plain_text = decode(encrypted)
    if not match(ur"^_*$", plain_text):
        table.append(u"<div class=\"pure-u-1-4\"><p>ENG</p></div>"
                     u"<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    plain_text = decode(" ".join(encrypted)
                        .translate({ord(u'.'): ord(u'-'),
                                    ord(u'-'): ord(u'.')})
                        .split())
    if not match(ur"^_*$", plain_text):
        table.append(u"<div class=\"pure-u-1-4\"><p>ENG rev</p></div>"
                     u"<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    letters = signs
    letters.update(ru)
    plain_text = decode(encrypted)
    if not match(ur"^_*$", plain_text):
        table.append(u"<div class=\"pure-u-1-4\"><p>RUS</p></div>"
                     u"<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    plain_text = decode(u" ".join(encrypted)
                        .translate({ord(u'.'): ord(u'-'),
                                    ord(u'-'): ord(u'.')})
                        .split())
    if not match(ur"^_*$", plain_text):
        table.append(u"<div class=\"pure-u-1-4\"><p>RUS rev</p></div>"
                     u"<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    if len(table) > 0:
        return (u"Morse",
                u"<div class=\"pure-g\">{}</div>".format(u"".join(table)))
    else:
        return "", ""


def from_hex(encrypted):
    try:
        return u"From HEX", u"".join(encrypted.split()).decode("hex")
    except ValueError:
        return "", ""


def from_ascii(encrypted):
    try:
        return (u"From ASCII",
                u"".join(map(chr, map(int, encrypted.split()))))
    except ValueError:
        return "", ""


def from_base64(encrypted):
    try:
        return u"From Base64", encrypted.decode("base64")
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
    table = []
    if rus:
        table.append(u"<div class=\"pure-u-1-4\"><p>RUS</p></div>"
                     u"<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(u"".join(rus)))
    if eng:
        table.append(u"<div class=\"pure-u-1-4\"><p>ENG</p></div>"
                     u"<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(u"".join(eng)))
    if len(table):
        return (u"From position",
                u"<div class=\"pure-g\">{}</div>".format(u"".join(table)))
    else:
        return "", ""


def from_binary(encrypted):
    """
    Binary decoder
    """
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
    plaintext = []

    encrypted = encrypted.lower()
    encrypted = sub("[^AB]", "", encrypted.strip())

    for i in range(len(encrypted) / 5):
        plaintext.append(BACONDICT.get(encrypted[i * 5:i * 5 + 5], '_'))
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
    table = []
    encrypted = unicode(encrypted)
    eng = findall("[A-Za-z]", encrypted)
    if len(eng) > 0:
        table.append(u"<div class=\"pure-u-1-3\"><p>ENG letters:</p></div>"
                     u"<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(u" ".join(eng)))
    rus = findall(u"[а-яёА-ЯЁ]", encrypted)
    if len(rus) > 0:
        table.append(u"<div class=\"pure-u-1-3\"><p>RUS letters:</p></div>"
                     u"<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(u" ".join(rus)))
    en_cap = findall("[A-Z]", encrypted)
    if len(en_cap) > 0:
        table.append(u"<div class=\"pure-u-1-3\"><p>EN Capital:</p></div>"
                     u"<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(u" ".join(en_cap)))
    ru_cap = findall(u"[А-ЯЁ]", encrypted)
    if len(ru_cap) > 0:
        table.append(u"<div class=\"pure-u-1-3\"><p>RUS Capital:</p></div>"
                     u"<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(u" ".join(ru_cap)))
    digits = findall(u"[0-9]", encrypted)
    if len(digits) > 0:
        table.append(u"<div class=\"pure-u-1-3\"><p>Digits:</p></div>"
                     u"<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(u" ".join(digits)))
    if len(table):
        return (u"Decapsulated",
                u"<div class=\"pure-g\">{}</div>".format(u"".join(table)))
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
                              data=payload).text
            if u"<b>Внимание!</b>" in r:
                return "", ""
            else:
                return u"Anagram", r.text
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
                             params=payload).text
            result = search(r"\d+ found\. Displaying all:\s*?</b>"
                            "<br>(.*?)<bottomlinks>", r, MULTILINE | DOTALL)
            return u"Anagram", result.group(1).replace("\n", "")
        except:
            pass
    return "", ""


def from_t9(encrypted):
    """
    Get text from T9
    """
    if not match(ur'^[\d\s]*$', unicode(encrypted)):
        return "", ""
    encrypted = unicode(encrypted).replace(u"0", " ")
    codes = map(list, encrypted.split())
    words = [[], []]
    for code in codes:
        prefix = [[], []]
        word = [[], []]
        for lang in [0, 1]:
            prefix[lang] = [phonepad[lang][int(digit)] for digit in code]
            for p in itertools.product(*prefix[lang]):
                p = u"".join(p)
                if p in dictionary[lang]:
                    word[lang].extend([p])
            words[lang].append(word[lang])

    table = []
    for lang in enumerate([u"EN", u"RU"]):
        if len(words[lang[0]]) == 0:
            continue
        table.append(u"<div class=\"pure-u-1-4\"><p>" + lang[1] +
                     u":</p></div><div class=\"pure-u-3-4\"><p>")
        for sentence in itertools.product(*filter(lambda x: len(x) > 0,
                                                  words[lang[0]])):
            table.append(u"{}<br>".format(u" ".join(sentence)))
        table[-1] = table[-1][:-4]
        table.append(u"</p></div>")
    if len(table):
        return (u"T9",
                u"<div class=\"pure-g\">{}</div>".format(u"".join(table)))
    else:
        return "", ""


functions = [
    morse,
    from_hex,
    from_ascii,
    from_binary,
    from_base64,
    from_position,
    keymap,
    reverse,
    decapsulate,
    anagram,
    bacon,
    caesar,
    atbash,
    from_t9,
]


def main():
    print u"This is not the function you are looking for!"


if __name__ == '__main__':
    main()
