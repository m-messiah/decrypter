# coding=utf-8
__author__ = 'messiah'

import unittest
from coordinates import Coordinates


class CoordinatesTestCase(unittest.TestCase):
    def test_dd2(self):
        """ DegDec to another  """

        dd = (u"56.829729", u"60.585864")
        dmr = u"56 49.784, 60 35.152"
        dmsr = u"56 49 47.02, 60 35 9.11"
        C = Coordinates(dd)
        self.assertEqual(C.all_coords["MinDec"], dmr)
        self.assertEqual(C.all_coords["DMS"], dmsr)

    def test_dm2(self):
        """ MinDec to another  """

        dm = (u"56 49.78374", u"60 35.15184")
        ddr = u"56.829729, 60.585864"
        dmsr = u"56 49 47.02, 60 35 9.11"
        C = Coordinates(dm)
        self.assertEqual(C.all_coords["DegDec"], ddr)
        self.assertEqual(C.all_coords["DMS"], dmsr)

    def test_dms2(self):
        """ DMS to another  """

        dms = (u"56 49 47.02", u"60 35 9.11")
        ddr = u"56.829728, 60.585864"
        dmr = u"56 49.784, 60 35.152"
        C = Coordinates(dms)
        self.assertEqual(C.all_coords["DegDec"], ddr)
        self.assertEqual(C.all_coords["MinDec"], dmr)

if __name__ == '__main__':
    unittest.main()
