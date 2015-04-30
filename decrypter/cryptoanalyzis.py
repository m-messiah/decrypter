# coding=utf-8
__author__ = 'm_messiah'
#RUS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RUS = (1072, 1073, 1074, 1075, 1076, 1077, 1105, 1078, 1079, 1080, 1081, 1082,
       1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094,
       1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103)
#ENG = "abcdefghijklmnopqrstuvwxyz"
ENG = (97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
       112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122)
BACONDICT = (dict(), dict())
for letter_counter in range(26):
    current_letter = (letter_counter - 2 if letter_counter > 20
                      else (letter_counter - 1 if letter_counter > 8
                            else letter_counter))
    tmp = bin(current_letter)[2:].zfill(5)
    tmp = tmp.replace('0', 'a')
    tmp = tmp.replace('1', 'b')
    tmp2 = bin(letter_counter)[2:].zfill(5)
    tmp2 = tmp2.replace('0', 'a')
    tmp2 = tmp2.replace('1', 'b')

    if current_letter in (8, 9):
        BACONDICT[0][tmp] = "I"
    elif current_letter in (19, 20):
        BACONDICT[0][tmp] = "U"
    else:
        BACONDICT[0][tmp] = chr(65 + letter_counter)
    BACONDICT[1][tmp2] = chr(65 + letter_counter)


dictionary = (frozenset(map(lambda x: x.rstrip(),
                        open("words/en.txt").readlines()
                        + open("words/tr.txt").readlines())),
              frozenset(map(lambda x: x.rstrip(),
                        open("words/ru.txt").readlines())))
# T9
phonepad = ((
            (" ",),
            ("",), ("a", "b", "c"), ("d", "e", "f"),
            ("g", "h", "i"), ("j", "k", "l"), ("m", "n", "o"),
            ("p", "q", "r", "s"), ("t", "u", "v"),
            ("w", "x", "y", "z")
            ),
            (
            (" ",), ("",),
            ("а", "б", "в", "г"), ("д", "е", "ж", "з"),
            ("и", "й", "к", "л"), ("м", "н", "о", "п"),
            ("р", "с", "т", "у"), ("ф", "х", "ц", "ч"),
            ("ш", "щ", "ъ", "ы"), ("ь", "э", "ю", "я")
            ))
# Morse
MORSE_EN = {
    '.....': '5', '-.--.-': '(', '..--..': '?', '.----': '1',
    '---...': ':', '......': '.', '----.': '9', '---..': '8',
    '..---': '2', '--..--': '!', '....-': '4', '-....': '6',
    '-.-.-.': ';', '-----': '0', '...--': '3',
    '.-..-.': '"', '--...': '7', '/': ' ', '.-.-.-': ',',
    '---': 'O', '--.': 'G', '-...': 'B', '-..-': 'X',
    '.-.': 'R', '--.-': 'Q', '--..': 'Z', '.--': 'W',
    '.-': 'A', '..': 'I', '-.-.': 'C', '..-.': 'F',
    '-.--': 'Y', '-': 'T', '.': 'E', '.-..': 'L', '...': 'S',
    '..-': 'U', '-.-': 'K', '-..': 'D', '.---': 'J',
    '.--.': 'P', '--': 'M', '-.': 'N', '....': 'H',
    '...-': 'V', '.----.': "'", '-....-': "–", '-..-.': "/", '.--.-.': "@"}

MORSE_RU = {
    '.....': '5', '-.--.-': '(', '..--..': '?', '.----': '1',
    '---...': ':', '......': '.', '----.': '9', '---..': '8',
    '..---': '2', '--..--': '!', '....-': '4', '-....': '6',
    '-.-.-.': ';', '-----': '0', '.-.-.-': ',', '...--': '3',
    '.-..-.': '"', '--...': '7', '/': ' ', '.----.': "'",
    "..-..": 'Э', "---": 'О', "--.": 'Г', "-...": 'Б',
    "-..-": 'Ь', ".-.": 'Р', "--.-": 'Щ', "--..": 'З',
    ".--": 'В', ".-": 'А', "..": 'И', "-.-.": 'Ц',
    "..-.": 'Ф', "..--": 'Ю', "-": 'Т', ".": 'Е',
    ".-.-": 'Я', ".-..": 'Л', "--.--": 'Ъ', "...": 'С',
    "..-": 'У', "----": 'Ш', "---.": 'Ч', "-.-": 'К',
    "-..": 'Д', ".---": 'Й', ".--.": 'П', "--": 'М',
    "-.": 'Н', "....": 'Х', "...-": 'Ж', "-.--": "Ы", '-....-': '–',
    '-..-.': '/', '.--.-.': '@'}

from re import sub, match, findall, compile
from itertools import product, permutations
from base64 import b64decode

eng_letters = compile(r"[a-z]")
rus_letters = compile(r"[а-яё]")

try:
    from decrypter import coordinates
except ImportError:
    import coordinates


def coords(encrypted):
    converted = coordinates.Coordinates(encrypted.split(',')).all_coords
    result = [
        "<div class=\"pure-u-1-4 descr\">%s</div>"
        "<div class=\"pure-u-3-4\">%s</div>" % (k, v)
        for k, v in sorted(converted.items())
    ]

    return ("Coordinates",
            "<div class=\"pure-g\">%s</div>" % "".join(result))


def caesar(encrypted):
    encrypted = encrypted.lower()
    if eng_letters.search(encrypted):
        abc = ENG
        language = dictionary[0]
    elif rus_letters.search(encrypted):
        abc = RUS
        language = dictionary[1]
    else:
        raise Exception("Not a words")

    decrypted = []
    for rot in range(1, len(abc)):
        key = abc[rot:] + abc[:rot]
        trans = dict(zip(abc, key))
        out = encrypted.translate(trans)
        if any(o in language for o in out.split()[:3]):
            decrypted.insert(0, (rot, out))
        else:
            decrypted.append((rot, out))

    return (
        "Caesar",
        "<div class=\"pure-g\">%s</div>" % "".join(
            map(lambda d:
                "<div class=\"pure-u-1-4 descr\">%sROT%s</div>"
                "<div class=\"pure-u-3-4\">%s</div>"
                % ("&nbsp;&nbsp;" if d[0] < 10 else "", d[0], d[1]),
                decrypted)))


def atbash(encrypted):
    encrypted = encrypted.lower()
    if eng_letters.search(encrypted):
        abc = ENG
    elif rus_letters.search(encrypted):
        abc = RUS
    else:
        raise Exception("Not a words")
    trans = dict(zip(abc, abc[::-1]))
    return "Atbash", encrypted.translate(trans)


def reverse(encrypted):
    return "Reversed text", encrypted[::-1]


def keymap(encrypted):
    #key = ("qwertyuiop[]asdfghjkl;'\<zxcvbnm,./`1234567890-="
    #       "~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|>ZXCVBNM<>?")
    key = (113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 97, 115,
           100, 102, 103, 104, 106, 107, 108, 59, 39, 92, 60, 122, 120, 99,
           118, 98, 110, 109, 44, 46, 47, 96, 49, 50, 51, 52, 53, 54, 55, 56,
           57, 48, 45, 61, 126, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41, 95,
           43, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 123, 125, 65, 83, 68,
           70, 71, 72, 74, 75, 76, 58, 34, 124, 62, 90, 88, 67, 86, 66, 78,
           77, 60, 62, 63)

    #abc = ("йцукенгшщзхъфывапролджэ\/ячсмитьбю.ё1234567890-="
    #       "Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/|ЯЧСМИТЬБЮ,")
    abc = (1081, 1094, 1091, 1082, 1077, 1085, 1075, 1096, 1097, 1079, 1093,
           1098, 1092, 1099, 1074, 1072, 1087, 1088, 1086, 1083, 1076, 1078,
           1101, 92, 47, 1103, 1095, 1089, 1084, 1080, 1090, 1100, 1073, 1102,
           46, 1105, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 1025, 33,
           34, 8470, 59, 37, 58, 63, 42, 40, 41, 95, 43, 1049, 1062, 1059,
           1050, 1045, 1053, 1043, 1064, 1065, 1047, 1061, 1066, 1060, 1067,
           1042, 1040, 1055, 1056, 1054, 1051, 1044, 1046, 1069, 47, 124,
           1071, 1063, 1057, 1052, 1048, 1058, 1068, 1041, 1070, 44)

    if eng_letters.search(encrypted):
        abc, key = key, abc
    trans = dict(zip(abc, key))
    return "Wrong Keymap", encrypted.translate(trans)


def morse(encrypted):
    encrypted = encrypted.split()

    def decode(text):
        return "".join(letters.get(c, "_") for c in text)

    def invert(word):
        # ord('-') = 45, ord('.') = 46
        return word.translate({46: 45, 45: 46})

    letters = MORSE_EN
    table = []
    plain_text = decode(encrypted)
    if any(c is not "_" for c in plain_text):
        table.extend(["<div class=\"pure-u-1-4 descr\">ENG</div>",
                      "<div class=\"pure-u-3-4\">",
                      plain_text, "</div>"])

    plain_text = decode(map(invert, encrypted))
    if any(c is not "_" for c in plain_text):
        table.extend(["<div class=\"pure-u-1-4 descr\">ENG rev</div>",
                     "<div class=\"pure-u-3-4\">",
                     plain_text, "</div>"])

    letters = MORSE_RU
    plain_text = decode(encrypted)
    if any(c is not "_" for c in plain_text):
        table.extend(["<div class=\"pure-u-1-4 descr\">RUS</div>",
                     "<div class=\"pure-u-3-4\">",
                     plain_text, "</div>"])

    plain_text = decode(map(invert, encrypted))
    if any(c is not "_" for c in plain_text):
        table.extend(["<div class=\"pure-u-1-4 descr\">RUS rev</div>",
                     "<div class=\"pure-u-3-4\">",
                     plain_text, "</div>"])

    assert len(table)
    return "Morse", "<div class=\"pure-g\">%s</div>" % "".join(table)


def from_hex(encrypted):
    r = bytes.fromhex(encrypted.replace(" ", ""))
    try:
        return "From HEX", r.decode("utf8")
    except UnicodeDecodeError:
        return "From HEX", r.decode("cp1251")


def from_dec(encrypted):
    r = bytes.fromhex(hex(int(encrypted.replace(" ", "")))[2:])
    try:
        return "From DEC", r.decode("utf8")
    except UnicodeDecodeError:
        return "From DEC", r.decode("cp1251")


def from_ascii(encrypted):
    return "From ASCII", "".join(map(chr, map(int, encrypted.split())))


def from_base64(encrypted):
    result = b64decode(encrypted.encode("utf8"))
    assert len(result)
    try:
        return "From Base64", result.decode("utf8")
    except UnicodeDecodeError:
        return "From Base64", result.decode("cp1251")


def from_position(encrypted):
    positions = list(map(int, encrypted.split()))
    rus = "".join(map(lambda i: chr(RUS[(i - 1) % 33]), positions))
    eng = "".join(map(lambda i: chr(ENG[(i - 1) % 26]), positions))
    return ("From position",
            """<div class="pure-g">
            <div class="pure-u-1-4 descr">RUS</div>
            <div class="pure-u-3-4">%s</div>
            <div class="pure-u-1-4 descr">ENG</div>
            <div class="pure-u-3-4">%s</div>
            </div>""" % (rus, eng))


def from_binary(encrypted):
    """
    Binary decoder
    """
    result = []
    for enc in encrypted.split():
        try:
            result.append(
                bytes.fromhex(hex(int("0b%s" % enc, 2))[2:]))
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
    result = ['<div class="pure-g">\n'
              '<div class="pure-u-1-4 descr">OLD</div> ',
              '<div class="pure-u-3-4">']

    encrypted = encrypted.lower()
    encrypted = sub("[^ab]", "", encrypted.strip())

    plaintext = [BACONDICT[0].get(encrypted[i * 5:i * 5 + 5], '_')
                 for i in range(len(encrypted) // 5)]
    assert len(plaintext)
    result.append("".join(plaintext))
    result.append("</div>\n")
    result.append('<div class="pure-u-1-4 descr">NEW</div> ')
    result.append('<div class="pure-u-3-4">')
    plaintext = [BACONDICT[1].get(encrypted[i * 5:i * 5 + 5], '_')
                 for i in range(len(encrypted) // 5)]
    assert len(plaintext)
    result.append("".join(plaintext))
    result.append("</div></div>%s" % BACONDICT[1])
    return "Bacon", "".join(result)


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
    eng = findall("[A-Za-z]", encrypted)
    if len(eng):
        table.extend(["<div class=\"pure-u-1-4 descr\">Eng</div>",
                      "<div class=\"pure-u-3-4\">",
                      " ".join(eng), "</div>"])

    rus = findall("[а-яёА-ЯЁ]", encrypted)
    if len(rus):
        table.extend(["<div class=\"pure-u-1-4 descr\">Rus</div>",
                      "<div class=\"pure-u-3-4\">",
                      " ".join(rus), "</div>"])

    en_cap = findall("[A-Z]", encrypted)
    if len(en_cap):
        table.extend(["<div class=\"pure-u-1-4 descr\">ENG</div>",
                      "<div class=\"pure-u-3-4\">",
                      " ".join(en_cap), "</div>"])

    ru_cap = findall("[А-ЯЁ]", encrypted)
    if len(ru_cap):
        table.extend(["<div class=\"pure-u-1-4 descr\">RUS</div>",
                      "<div class=\"pure-u-3-4\">",
                      " ".join(ru_cap), "</div>"])

    digits = findall("[0-9]", encrypted)
    if len(digits):
        table.extend(["<div class=\"pure-u-1-4 descr\">0-9</div>",
                      "<div class=\"pure-u-3-4\">",
                     " ".join(digits), "</div>"])

    assert len(table)
    return ("Decapsulated",
            "<div class=\"pure-g\">%s</div>" % "".join(table))


def from_t9(encrypted):
    """
    Get text from T9
    """
    assert match(r'^[\d\s]*$', encrypted)
    encrypted = encrypted.replace("0", " ")
    encrypted_array = encrypted.split()
    assert (sum(map(len, encrypted_array))
            / len(encrypted_array) < 3 < len(encrypted_array))
    words = [[], []]
    for code in encrypted.split():
        prefix = [[], []]
        word = [[], []]
        for lang in [0, 1]:
            prefix[lang] = [phonepad[lang][int(digit)] for digit in code]
            for p in product(*prefix[lang]):
                p = "".join(p)
                if p in dictionary[lang]:
                    word[lang].append(p)
            words[lang].append(word[lang])

    table = []
    for lang in enumerate(("EN", "RU")):
        if len(words[lang[0]]) == 0:
            continue
        table.extend(["<div class=\"pure-u-1-4 descr\">", lang[1],
                      "</div><div class=\"pure-u-3-4\">"])
        for sentence in product(*filter(lambda x: bool(x), words[lang[0]])):
            table.append(" ".join(sentence))
            table.append("<br>")
        table[-1] = "</div>"
    assert len(table)
    return "T9", "<div class=\"pure-g\">%s</div>" % "".join(table)


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
    bacon,
    atbash,
    caesar,
    from_t9,
]


def main():
    raise Exception("This is not the function you are looking for!")


if __name__ == '__main__':
    main()
