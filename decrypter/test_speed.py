__author__ = 'm_messiah'

try:
    from decrypter import cryptoanalyzis
except ImportError:
    import cryptoanalyzis
import cProfile

def decrypt(encrypted):
    decrypted = []
    for func in cryptoanalyzis.functions:
        try:
            decrypted.append(func(encrypted))
        except:
            continue
    return decrypted


cProfile.runctx('decrypt("hello123")', None, locals())
