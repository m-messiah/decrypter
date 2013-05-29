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


def morse(encrypted):
    signs = [
        (',', "-.-.-.-"), (';', "-.-.-."), (':', "---..."), ('!', "--..--"),
        ('?', "..--.."), ('.', "......"), ("'", ".-..-."), ('(', "-.--.-"),
        ('0', "-----"), ('1', ".----"), ('2', "..---"), ('3', "...--"),
        ('4', "....-"), ('5', "....."), ('6', "-...."), ('7', "--..."),
        ('8', "---.."), ('9', "----.")]

    en = [
        ('A', ".-"), ('B', "-..."), ('C', "-.-."), ('D', "-.."), ('E', "."),
        ('F', "..-."), ('G', "--."), ('H', "...."), ('I', ".."), ('J', ".---"),
        ('K', "-.-"), ('L', ".-.."), ('M', "--"), ('N', "-."), ('O', "---"),
        ('P', ".--."), ('Q', "--.-"), ('R', ".-."), ('S', "..."), ('T', "-"),
        ('U', "..-"), ('V', "...-"), ('W', ".--"), ('X', "-..-"), ('Y', "-.--"),
        ('Z', "--..")]

    ru = [
        ('А', ".-"), ('Б', "-..."), ('В', ".--"), ('Г', "--."), ('Д', "-.."),
        ('Е', "."), ('Ж', "...-"), ('З', "--.."), ('И', ".."),
        ('Й', ".---"), ('К', "-.-"), ('Л', ".-.."), ('М', "--"), ('Н', "-."),
        ('О', "---"), ('П', ".--."), ('Р', ".-."), ('С', "..."), ('Т', "-"),
        ('У', "..-"), ('Ф', "..-."), ('Х', "...."), ('Ц', "-.-."),
        ('Ч', "---."), ('Ъ', "--.--"),
        ('Ш', "----"), ('Щ', "--.-"), ('Ы', "--.-"), ('Ь', "-..-"),
        ('Э', "..-.."), ('Ю', "..--"), ('Я', ".-.-")]

    encrypted = u"{}".format(encrypted).lower()

    def decode(input):
        if input == "":
            return [""]
        else:
            return [letter + remaining
                    for letter, code in letters if input.startswith(code)
                    for remaining in decode(input[len(code):])]

    letters = signs + en
    eng = u"<tr><th>ENG</th><td>{}</td></tr>".format(decode(encrypted))
    letters = signs + ru
    rus = u"<tr><th>RUS</th><td>{}</td></tr>".format(decode(encrypted))
    return "Morse", u"<table>{}{}</table>".format(eng, rus)


functions = [
    caesar,
    morse,
]


def main():
    pass


if __name__ == '__main__':
    main()
