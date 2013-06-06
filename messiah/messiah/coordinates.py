# -*- coding: utf-8 -*-
__author__ = 'Messiah'


class Coordinates(object):
    def __init__(self, coords):
        self.typeCoords = ["BadInput", "DegDec", "MinDec", "DMS"]
        self.type, self.coords = self.parse(coords)
        self.allCoords = {"DegDec": [], "MinDec": [], "DMS": []}
        self.convert()

    def parse(self, coords):
        coords = coords.split(",")
        max = 0
        result = [0, [[], []]]
        for lat, i in zip(coords, range(len(coords))):
            lat = lat.split()
            count = len(lat)
            if count > max:
                max = count
            result[1][i] = lat
        result[0] = self.typeCoords[max]
        return result

    def degDec2MinDec(self):
        result = []
        for lat, i in zip(self.coords, range(2)):
            lat = float(lat[0])
            d = int(lat)
            m = abs((lat - d) * 60)
            if i == 0:
                l = "N" if lat > 0 else "S"
            if i > 0:
                l = "E" if lat > 0 else "W"
            result.append("{}°{}\'{}".format(abs(d), m, l))
        return "{}, {}".format(result[0], result[1])

    def degDec2DMS(self):
        result = []
        for lat, i in zip(self.coords, range(2)):
            lat = float(lat[0])
            d = int(lat)
            ms = abs((lat - d) * 60)
            m = int(ms)
            s = round((ms - m) * 60, 2)
            if i == 0:
                l = "N" if lat > 0 else "S"
            if i > 0:
                l = "E" if lat > 0 else "W"
            result.append("{}°{}\'{}\"{}".format(abs(d), m, s, l))
        return "{}, {}".format(result[0], result[1])

    def minDec2DegDec(self):
        result = []
        for lat in self.coords:
            d, m = map(float, lat)
            modul = abs(d) + m / 60
            if d < 0:
                modul *= -1
            result.append(modul)
        return "{}, {}".format(result[0], result[1])

    def minDec2DMS(self):
        result = []
        for lat in self.coords:
            d, ms = map(float, lat)
            m = int(ms)
            s = round((ms - m) * 60, 2)
            result.append("{}°{}\'{}\"".format(int(d), m, s))
        return "{}, {}".format(result[0], result[1])

    def dMS2DegDec(self):
        result = []
        for lat in self.coords:
            d, m, s = map(float, lat)
            modul = abs(d) + (m * 60 + s) / 3600
            if d < 0:
                modul *= -1
            result.append(modul)
        return "{}, {}".format(result[0], result[1])

    def dMS2MinDec(self):
        result = []
        for lat in self.coords:
            d, m, s = map(float, lat)
            result.append("{}°{}\'".format(int(d), m + s / 60))
        return "{}, {}".format(result[0], result[1])

    def dms(self, i):
        d, m, s = self.coords[i]
        lat = ["N", "E"]
        return "{}°{}\'{}\"{}".format(d, m, s, lat[i])

    def mindec(self, i):
        d, m = self.coords[i]
        return "{}° {}".format(d, m)

    def convert(self):
        if self.type == "DMS":
            self.allCoords["DMS"] = "{}, {}".format(self.dms(0), self.dms(1))
            self.allCoords["MinDec"] = self.dMS2MinDec()
            self.allCoords["DegDec"] = self.dMS2DegDec()
        elif self.type == "MinDec":
            self.allCoords["MinDec"] = "{}, {}".format(self.mindec(0),
                                                       self.mindec(1))
            self.allCoords["DMS"] = self.minDec2DMS()
            self.allCoords["DegDec"] = self.minDec2DegDec()
        elif self.type == "DegDec":
            self.allCoords["DegDec"] = "{0[0]}, {1[0]}".format(*self.coords)
            self.allCoords["MinDec"] = self.degDec2MinDec()
            self.allCoords["DMS"] = self.degDec2DMS()
        else:
            self.allCoords["BadInput"] = 0
        degDec = self.allCoords["DegDec"].split(",")
        links = []
        links.append("<a href=\"http://maps.google.com/maps?"
                     "q=loc:{},{}&z=15\" class='btn'"
                     "target='_blank'>GoogleMaps</a>"
                     .format(degDec[0], degDec[1].strip()))
        self.allCoords["~ Maps"] = " ".join(links)

    def __str__(self):
        res = ["------"]
        for k, v in self.allCoords.items():
            res.append("{} : {}".format(k, v))
        return "\n".join(res)


if __name__ == "__main__":
    from sys import argv
    print Coordinates(argv[1])
