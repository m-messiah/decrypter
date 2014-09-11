# coding=utf-8
__author__ = 'm_messiah'

import unittest
import codecs

from cryptoanalyzis import *


class CryptoTestCase(unittest.TestCase):
    def test_caesar(self):
        self.assertTrue(codecs.encode("hellowor", "rot13")
                        in caesar("hellowor")[1])
        self.assertTrue(u"".join(map(lambda x: chr(ord(x) + 3), u"привким"))
                        in caesar(u"привким")[1])

    def test_binary(self):
        self.assertEqual(
            "hello",
            from_binary("01101000 01100101 01101100 01101100 01101111")[1]
        )

    def test_hex(self):
        self.assertEqual("hello", from_hex("68656c6c6f")[1])

    def test_pos(self):
        self.assertTrue("hello" in from_position("8 5 12 12 15")[1])

    def test_ascii(self):
        self.assertEqual("hello",
                         from_ascii(" ".join(map(str, map(ord, "hello"))))[1])

    def test_base64(self):
        self.assertEqual("hello", from_base64("aGVsbG8=")[1])

    def test_keymap(self):
        self.assertEqual("hello", keymap("руддщ")[1])

    def test_reverse(self):
        self.assertEqual("hello", reverse("olleh")[1])

    def test_morse(self):
        self.assertTrue("hello" in morse(".... . .-.. .-.. ---")[1].lower())



if __name__ == '__main__':
    unittest.main()
