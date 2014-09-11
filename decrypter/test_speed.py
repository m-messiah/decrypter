__author__ = 'm_messiah'

try:
    from decrypter import cryptoanalyzis
except ImportError:
    import cryptoanalyzis


def decrypter(encrypted):
    decrypted = []
    for func in cryptoanalyzis.functions:
        try:
            decrypted.append(func(encrypted))
        except:
            continue
    return decrypted


print(decrypter("oehll"))
#import cProfile
#cProfile.run('decrypter("hello123")')