# coding=utf-8
import base64

__author__ = 'm_messiah'
RUS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENG = "abcdefghijklmnopqrstuvwxyz"
BACONDICT = {}
for letter_counter in range(26):
    if letter_counter in [9, 21]:
        continue
    current_letter = (letter_counter - 2 if letter_counter > 20
                      else (letter_counter - 1 if letter_counter > 8
                            else letter_counter))
    tmp = bin(current_letter)[2:].zfill(5)
    tmp = tmp.replace('0', 'a')
    tmp = tmp.replace('1', 'b')
    BACONDICT[tmp] = chr(65 + letter_counter)

dictionary = [set(map(lambda x: x.rstrip(),
                      open("words/en.txt").readlines())).union(
              set(map(lambda x: x.rstrip(),
                      open("words/tr.txt").readlines()))),
              set(map(lambda x: x.rstrip(),
                      open("words/ru.txt").readlines()))]

phonepad = [[
            [" "],
            [""], ["a", "b", "c"], ["d", "e", "f"],
            ["g", "h", "i"], ["j", "k", "l"], ["m", "n", "o"],
            ["p", "q", "r", "s"], ["t", "u", "v"],
            ["w", "x", "y", "z"]
            ],
            [
            [" "], [""],
            ["а", "б", "в", "г"], ["д", "е", "ж", "з"],
            ["и", "й", "к", "л"], ["м", "н", "о", "п"],
            ["р", "с", "т", "у"], ["ф", "х", "ц", "ч"],
            ["ш", "щ", "ъ", "ы"], ["ь", "э", "ю", "я"]
            ]]

signs = {'.....': '5', '-.--.-': '(', '..--..': '?', '.----': '1',
         '---...': ':', '......': '.', '----.': '9', '---..': '8',
         '..---': '2', '-.-.--': '!', '....-': '4', '-....': '6',
         '-.-.-.': ';', '-----': '0', '-.-.-.-': ',', '...--': '3',
         '.-..-.': "'", '--...': '7', '/': ' ', '--..--': ','}

en = {'---': 'O', '--.': 'G', '-...': 'B', '-..-': 'X',
      '.-.': 'R', '--.-': 'Q', '--..': 'Z', '.--': 'W',
      '.-': 'A', '..': 'I', '-.-.': 'C', '..-.': 'F',
      '-.--': 'Y', '-': 'T', '.': 'E', '.-..': 'L', '...': 'S',
      '..-': 'U', '-.-': 'K', '-..': 'D', '.---': 'J',
      '.--.': 'P', '--': 'M', '-.': 'N', '....': 'H',
      '...-': 'V'}

ru = {"..-..": 'Э', "---": 'О', "--.": 'Г', "-...": 'Б',
      "-..-": 'Ь', ".-.": 'Р', "--.-": 'Ы', "--..": 'З',
      ".--": 'В', ".-": 'А', "..": 'И', "-.-.": 'Ц',
      "..-.": 'Ф', "..--": 'Ю', "-": 'Т', ".": 'Е',
      ".-.-": 'Я', ".-..": 'Л', "--.--": 'Ъ', "...": 'С',
      "..-": 'У', "----": 'Ш', "---.": 'Ч', "-.-": 'К',
      "-..": 'Д', ".---": 'Й', ".--.": 'П', "--": 'М',
      "-.": 'Н', "....": 'Х', "...-": 'Ж'}

from re import search, sub, match, findall
from itertools import product, permutations
try:
    from decrypter import coordinates
except ImportError:
    import coordinates


def coords(encrypted):
    converted = coordinates.Coordinates(encrypted.split(',')).all_coords
    result = [
        "<div class=\"pure-u-1-4 descr\">{}</div>"
        "<div class=\"pure-u-3-4\">{}</div>".format(k, v)
        for k, v in sorted(converted.items())
    ]

    return ("Coordinates",
            "<div class=\"pure-g\">{}</div>".format("".join(result)))


def caesar(encrypted):
    encrypted = encrypted.lower()
    if search(r"[a-z]", encrypted):
        abc = ENG
        language = dictionary[0]
    elif search(r"[а-яё]", encrypted):
        abc = RUS
        language = dictionary[1]
    else:
        raise Exception("Not a words")

    decrypted = []
    for rot in range(1, len(abc)):
        key = abc[rot:] + abc[:rot]
        trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
        out = encrypted.translate(trans)
        if any(o in language for o in out.split()[:5]):
            decrypted = [(rot, out)] + decrypted
        else:
            decrypted.append((rot, out))

    return (
        "Caesar",
        "<div class=\"pure-g\">{}</div>".format(
            "".join(
                map(lambda d:
                    "<div class=\"pure-u-1-4 descr\">{}ROT{}</div>"
                    "<div class=\"pure-u-3-4\">{}</div>"
                    .format("&nbsp;&nbsp;" if d[0] < 10 else "", d[0], d[1]),
                    decrypted))))


def atbash(encrypted):
    encrypted = encrypted.lower()
    if search(r"[a-z]", encrypted):
        abc = ENG
    elif search(r"[а-яё]", encrypted):
        abc = RUS
    else:
        raise Exception("Not a words")
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, abc[::-1]))
    return ("Atbash",
            "{}".format(encrypted.translate(trans)))


def reverse(encrypted):
    return "Reversed text", encrypted[::-1]


def keymap(encrypted):
    encrypted = encrypted
    key = ("qwertyuiop[]asdfghjkl;'\<zxcvbnm,./`1234567890-="
           "~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|>ZXCVBNM<>?")
    abc = ("йцукенгшщзхъфывапролджэ\/ячсмитьбю.ё1234567890-="
           "Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/|ЯЧСМИТЬБЮ,")
    if search(r"[a-z]", encrypted):
        abc, key = key, abc
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    return "Wrong Keymap", "{}".format(encrypted.translate(trans))


def morse(encrypted):
    encrypted = encrypted.split()

    def decode(text):
        result = []
        for c in text:
            try:
                result.append(letters[c])
            except KeyError:
                result.append("_")
        return "".join(result)

    def invert(word):
        return word.translate({ord('.'): ord('-'),
                               ord('-'): ord('.')})

    letters = signs
    letters.update(en)
    table = []
    plain_text = decode(encrypted)
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4 descr\">ENG</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(plain_text))
    plain_text = decode(map(invert, encrypted))
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4 descr\">ENG rev</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(plain_text))
    letters = signs
    letters.update(ru)
    plain_text = decode(encrypted)
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4 descr\">RUS</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(plain_text))
    plain_text = decode(map(invert, encrypted))
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4 descr\">RUS rev</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(plain_text))
    assert len(table)
    return "Morse", "<div class=\"pure-g\">{}</div>".format("".join(table))


def from_hex(encrypted):
    r = bytes.fromhex("".join(encrypted.split()))
    try:
        return "From HEX", r.decode("utf8")
    except UnicodeDecodeError:
        return "From HEX", r.decode("cp1251")


def from_ascii(encrypted):
    return "From ASCII", "".join(map(chr, map(int, encrypted.split())))


def from_base64(encrypted):
    result = base64.b64decode(encrypted.encode("utf8"))
    assert len(result)
    try:
        return "From Base64", result.decode("utf8")
    except UnicodeDecodeError:
        return "From Base64", result.decode("cp1251")


def from_position(encrypted):
    positions = list(map(int, encrypted.split()))
    rus = "".join(map(lambda i: RUS[(i - 1) % 33], positions))
    eng = "".join(map(lambda i: ENG[(i - 1) % 26], positions))
    return ("From position",
            """<div class="pure-g">
            <div class="pure-u-1-4 descr">RUS</div>
            <div class="pure-u-3-4">{}</div>
            <div class="pure-u-1-4 descr">ENG</div>
            <div class="pure-u-3-4">{}</div>
            </div>""".format(rus, eng))


def from_binary(encrypted):
    """
    Binary decoder
    """
    result = []
    for enc in encrypted.split():
        try:
            result.append(
                bytes.fromhex("%x" % int("0b{}".format(enc), 2)))
        except ValueError:
            pass
    assert len(result)
    try:
        return "From BIN", "".join(map(lambda x: x.decode("utf8"), result))
    except UnicodeDecodeError:
        return "From BIN", "".join(map(lambda x: x.decode("cp1251"), result))


def bacon(encrypted):
    """
    Bacon cipher (http://www.cs.ucf.edu/~gworley/files/baconian_cipher.txt)
    :param encrypted:
    """
    plaintext = []

    encrypted = encrypted.lower()
    encrypted = sub("[^ab]", "", encrypted.strip())

    for i in range(len(encrypted) // 5):
        plaintext.append(BACONDICT.get(encrypted[i * 5:i * 5 + 5], '_'))
    plaintext = "".join(plaintext)
    assert match(r"_*", plaintext) and len(plaintext)
    return "Bacon", plaintext


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
    encrypted = encrypted
    eng = findall("[A-Za-z]", encrypted)
    if len(eng):
        table.append("<div class=\"pure-u-1-4 descr\">Eng</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(" ".join(eng)))
    rus = findall("[а-яёА-ЯЁ]", encrypted)
    if len(rus):
        table.append("<div class=\"pure-u-1-4 descr\">Rus</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(" ".join(rus)))
    en_cap = findall("[A-Z]", encrypted)
    if len(en_cap):
        table.append("<div class=\"pure-u-1-4 descr\">ENG</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(" ".join(en_cap)))
    ru_cap = findall("[А-ЯЁ]", encrypted)
    if len(ru_cap):
        table.append("<div class=\"pure-u-1-4 descr\">RUS</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(" ".join(ru_cap)))
    digits = findall("[0-9]", encrypted)
    if len(digits):
        table.append("<div class=\"pure-u-1-4 descr\">0-9</div>"
                     "<div class=\"pure-u-3-4\">{}</div>"
                     .format(" ".join(digits)))
    assert len(table)
    return ("Decapsulated",
            "<div class=\"pure-g\">{}</div>".format("".join(table)))


def anagram(encrypted):
    """
    Do the anagram search.
    :param encrypted:
    """
    if match(r"^[А-Яа-яёЁ]+$", encrypted):
        lang = 1
    elif match(r"^[A-Za-z]+$", encrypted):
        lang = 0
    else:
        raise Exception("Not a words")
    result = set()
    for word in permutations(encrypted):
        word = "".join(word)
        if word in dictionary[lang]:
            result.add(word)
    assert len(result)
    return "Anagram", "<br>".join(result)


def from_t9(encrypted):
    """
    Get text from T9
    """
    assert match(r'^[\d\s]*$', encrypted)
    encrypted = encrypted.replace("0", " ")
    codes = map(list, encrypted.split())
    words = [[], []]
    for code in codes:
        prefix = [[], []]
        word = [[], []]
        for lang in [0, 1]:
            prefix[lang] = [phonepad[lang][int(digit)] for digit in code]
            for p in product(*prefix[lang]):
                p = "".join(p)
                if p in dictionary[lang]:
                    word[lang].extend([p])
            words[lang].append(word[lang])

    table = []
    for lang in enumerate(["EN", "RU"]):
        if len(words[lang[0]]) == 0:
            continue
        table.append("<div class=\"pure-u-1-4 descr\">" + lang[1] +
                     "</div><div class=\"pure-u-3-4\">")
        for sentence in product(*filter(lambda x: len(x) > 0,
                                        words[lang[0]])):
            table.append("{}<br>".format(" ".join(sentence)))
        table[-1] = table[-1][:-4]
        table.append("</div>")
    assert len(table)
    return "T9", "<div class=\"pure-g\">{}</div>".format("".join(table))


functions = [
    coords,
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
    atbash,
    caesar,
    from_t9,
]


def main():
    raise Exception("This is not the function you are looking for!")


if __name__ == '__main__':
    main()
