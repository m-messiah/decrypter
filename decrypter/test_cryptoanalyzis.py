# coding=utf-8
__author__ = 'messiah'

import unittest
from cryptoanalyzis import *


class CryptoTestCase(unittest.TestCase):
    def test_caesar(self):
        self.assertTrue("hellowor".encode("rot13") in caesar("hellowor")[1])
        self.assertTrue(u"".join(map(lambda x: unichr((ord(x) + 3)),
                                     u"привким"))
                        in caesar(u"привким")[1])

if __name__ == '__main__':
    unittest.main()
