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

from re import search, sub, match, findall, MULTILINE, DOTALL
import requests
import itertools
from decrypter import coordinates


def coords(encrypted):
    converted = coordinates.Coordinates(encrypted.split(',')).all_coords
    result = [
        "<div class=\"pure-u-1-4\">{}</div>"
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
        if any(o in language for o in out.split()):
            decrypted = [(rot, out)] + decrypted
        else:
            decrypted.append((rot, out))

    return (
        "<abbr title=\"Cyclic shift\">Caesar</abbr>",
        "<div class=\"pure-g\">{}</div>".format(
            "".join(
                map(lambda d:
                    "<div class=\"pure-u-1-3\"><p>ROT{}</p></div>"
                    "<div class=\"pure-u-2-3\"><p>{}</p></div>"
                    .format(d[0], d[1]), decrypted))))


def atbash(encrypted):
    encrypted = encrypted.lower()
    if search(r"[a-z]", encrypted):
        abc = ENG
    elif search(r"[а-яё]", encrypted):
        abc = RUS
    else:
        raise Exception("Not a words")
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, abc[::-1]))
    return ("<abbr title=\"A=Z B=Y...Y=B,Z=A\">Atbash</abbr>",
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
        table.append("<div class=\"pure-u-1-4\"><p>ENG</p></div>"
                     "<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    plain_text = decode(map(invert, encrypted))
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4\"><p>ENG rev</p></div>"
                     "<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    letters = signs
    letters.update(ru)
    plain_text = decode(encrypted)
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4\"><p>RUS</p></div>"
                     "<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    plain_text = decode(map(invert, encrypted))
    if not match(r"^_*$", plain_text):
        table.append("<div class=\"pure-u-1-4\"><p>RUS rev</p></div>"
                     "<div class=\"pure-u-3-4\"><p>{}</p></div>"
                     .format(plain_text))
    assert len(table)
    return "Morse", "<div class=\"pure-g\">{}</div>".format("".join(table))


def from_hex(encrypted):
    return ("From HEX",
            bytes.fromhex("".join(encrypted.split())).decode("utf-8"))


def from_ascii(encrypted):
    return "From ASCII", "".join(map(chr, map(int, encrypted.split())))


def from_base64(encrypted):
    result = base64.b64decode(encrypted.encode("utf8"))
    assert len(result)
    return "From Base64", result.decode("utf8")


def from_position(encrypted):
    positions = list(map(int, encrypted.split()))
    rus = "".join(map(lambda i: RUS[(i - 1) % 33], positions))
    eng = "".join(map(lambda i: ENG[(i - 1) % 26], positions))
    return ("From position",
            """<div class="pure-g">
            <div class="pure-u-1-4"><p>RUS</p></div>
            <div class="pure-u-3-4"><p>{}</p></div>
            <div class="pure-u-1-4"><p>ENG</p></div>
            <div class="pure-u-3-4"><p>{}</p></div>
            </div>""".format(rus, eng))


def from_binary(encrypted):
    """
    Binary decoder
    """
    import binascii
    result = []
    for enc in encrypted.split():
        try:
            result.append(
                binascii.unhexlify("%x" % int("0b{}".format(enc), 2))
                .decode("utf8"))
        except ValueError:
            pass
    assert len(result)
    return "From BIN", "".join(result)


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
    return "<abbr title=\"AAABBBABAA\">Bacon</abbr>", plaintext


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
        table.append("<div class=\"pure-u-1-3\"><p>ENG letters:</p></div>"
                     "<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(" ".join(eng)))
    rus = findall("[а-яёА-ЯЁ]", encrypted)
    if len(rus):
        table.append("<div class=\"pure-u-1-3\"><p>RUS letters:</p></div>"
                     "<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(" ".join(rus)))
    en_cap = findall("[A-Z]", encrypted)
    if len(en_cap):
        table.append("<div class=\"pure-u-1-3\"><p>EN Capital:</p></div>"
                     "<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(" ".join(en_cap)))
    ru_cap = findall("[А-ЯЁ]", encrypted)
    if len(ru_cap):
        table.append("<div class=\"pure-u-1-3\"><p>RUS Capital:</p></div>"
                     "<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(" ".join(ru_cap)))
    digits = findall("[0-9]", encrypted)
    if len(digits):
        table.append("<div class=\"pure-u-1-3\"><p>Digits:</p></div>"
                     "<div class=\"pure-u-2-3\"><p>{}</p></div>"
                     .format(" ".join(digits)))
    assert len(table)
    return ("Decapsulated",
            "<div class=\"pure-g\">{}</div>".format("".join(table)))


def anagram(encrypted):
    """
    Do the anagram search.
    Russian on 4maf.ru (thanks to authors)
    English on wordsmith.org (thanks, community!)
    :param encrypted:
    """
    encrypted = encrypted
    if match(r"[А-Яа-яёЁ]+", encrypted):
        payload = {
            "sourceword": encrypted,
            "ModType": 1,
            "minf": 0
        }
        r = requests.post("http://4maf.ru/anagram_ajax.php",
                          data=payload).text
        assert "<b>Внимание!</b>" not in r
        return "Anagram", r.text

    elif match(r"[A-Za-z]+", encrypted):
        payload = {
            "anagram": encrypted,
            "t": 50,
            "a": "n"
        }
        r = requests.get("http://www.wordsmith.org/anagram/anagram.cgi",
                         params=payload).text
        result = search(r"\d+ found\. Displaying all:\s*?</b>"
                        "<br>(.*?)<bottomlinks>", r, MULTILINE | DOTALL)
        return "Anagram", result.group(1).replace("\n", "")
    else:
        raise Exception("Not a words")


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
            for p in itertools.product(*prefix[lang]):
                p = "".join(p)
                if p in dictionary[lang]:
                    word[lang].extend([p])
            words[lang].append(word[lang])

    table = []
    for lang in enumerate(["EN", "RU"]):
        if len(words[lang[0]]) == 0:
            continue
        table.append("<div class=\"pure-u-1-4\"><p>" + lang[1] +
                     ":</p></div><div class=\"pure-u-3-4\"><p>")
        for sentence in itertools.product(*filter(lambda x: len(x) > 0,
                                                  words[lang[0]])):
            table.append("{}<br>".format(" ".join(sentence)))
        table[-1] = table[-1][:-4]
        table.append("</p></div>")
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
