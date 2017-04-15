#-*- coding: utf-8 -*-
import signal, unittest
from datetime import datetime
from inspect import getargspec
from coordinates_extractor import extract_coordinates, extract_first_coordinate_pair_from_list
from os.path import abspath, dirname, join, realpath
from requests import get
from unittest import TestCase

path_to_directory_of_this_file = dirname(realpath(__file__))
class Test(TestCase):

    #def test_local_african_pdf(self):
    #    locations = extract_locations_with_context(path_to_file, debug=True)
    #    self.assertEqual(len(locations) > 5)

    def test_1(self):
        line = '{{Coord|32.7|-86.7|type:adm2nd_dim:1000000_source:USGS|display=title}}&lt;!-- geographic center of state --&gt;\n'
        coordinates = extract_coordinates(line)
        self.assertEqual(coordinates['latitude'], 32.7)
        self.assertEqual(coordinates['longitude'], -86.7)

    def test_dms(self):
        line = '|coordinates = {{coord|57|9|3.6|N|2|7|22.8|W|type:adm2nd_region:GB|format=dms|display=inline,title}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(round(coordinates['latitude'], 3), 57.151)
        self.assertEqual(round(coordinates['longitude'], 3), -2.123)

    def test_alaska(self):
        line = "{{Coord|64|N|150|W|region:US-AK_type:adm1st_scale:10000000|display=title|notes=&lt;ref&gt;{{Cite gnis|1785533|State of Alaska}}&lt;/ref&gt;}}\n"
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(round(coordinates['latitude'], 3), 64)
        self.assertEqual(round(coordinates['longitude'], 3), -150)

    def test_adelaida(self):
        lines = ['| latd  = 34  | latm  = 55 | lats  = 44.4\n', '| longd = 138 | longm = 36 | longs = 3.6\n']
        coordinates = extract_coordinates(lines[0], debug=False)
        self.assertEqual(coordinates['latitude'], 34.928999999999995)

        coordinates = extract_coordinates(lines[1], debug=False)
        self.assertEqual(coordinates['longitude'], 138.601)

        coordinates = extract_first_coordinate_pair_from_list(lines, debug=False)
        self.assertEqual(coordinates['latitude'], 34.928999999999995)
        self.assertEqual(coordinates['longitude'], 138.601)

    def test_anguila(self):
        line = '{{Coord|18.22723|N|63.04899|W|type:landmark_scale:5000|display=title}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 18.22723)
        self.assertEqual(coordinates['longitude'], -63.04899)

    def test_aelia(self):
        line = '|coordinates = {{coord|31.775689|35.23104|display=inline}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 31.775689)
        self.assertEqual(coordinates['longitude'], 35.23104)

    def test_waterloo(self):
        line = '|coordinates = {{Coord|50.68016|N| 4.41169|E|region:BE_type:event|display=inline,title}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 50.68016)
        self.assertEqual(coordinates['longitude'], 4.41169)




if __name__ == '__main__':
    unittest.main()
