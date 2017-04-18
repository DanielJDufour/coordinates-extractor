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

    def test_great_victoria_desert(self):
        line = '{{Coord|29.1521612833|S|129.259643555|E|source:dewiki_region:AU_scale:7000000_type:landmark|format=dms|display=title}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], -29.1521612833)
        self.assertEqual(coordinates['longitude'], 129.259643555)

    def test_idaho(self):
        line = '{{Coord|display=title|45|N|114|W|region:US-ID_type:adm1st_scale:3000000}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 45)
        self.assertEqual(coordinates['longitude'], -114)

    def test_paris_texas(self):
        line = '{{Coord|display=title|33.662508|-95.547692}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 33.662508)
        self.assertEqual(coordinates['longitude'], -95.547692)

    def test_template_of_jerusalem(self):
        line = '{{Coord|31.77765|N|35.23547|E |format=dms |region:IL_type:landmark_source:placeopedia |display=title}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 31.77765)
        self.assertEqual(coordinates['longitude'], 35.23547)

    def test_geography_of_switzerland(self):
        line = '|coordinates = 47\xc2\xb0 N 8\xc2\xb0 E\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 47)
        self.assertEqual(coordinates['longitude'], 8)

    def test_hartford(self):
        line = '{{Coord|display=title|41.762736| -72.674286}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 41.762736)
        self.assertEqual(coordinates['longitude'], -72.674286)

    def test_beverly_ma(self):
        line = '{{Coord|42.558&lt;!--4284--&gt;|-70.880&lt;!--0491--&gt;|region:US_type:landmark|display=title}} &lt;!-- see usgs gnis in references --&gt;\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 42.558)
        self.assertEqual(coordinates['longitude'], -70.880)

    def test_old_firm(self):
        try:
            lines = ['| latd1  = 55 | latm1  = 50 | lats1  = 59    | latNS1  = N\n', '| longd1 =  4 | longm1 = 12 | longs1 = 20    | longEW1 = W\n', '| latd2  = 55 | latm2  = 51 | lats2  = 11.54 | latNS2  = N\n', '| longd2 =  4 | longm2 = 18 | longs2 = 33.33 | longEW2 = W\n']
            print "lines:", lines
            coordinates = extract_first_coordinate_pair_from_list(lines, debug=False)
            print "coords:", coordinates
            self.assertEqual(coordinates['latitude'], 55.849722222222226)
            self.assertEqual(coordinates['longitude'], 4.205555555555556)
        except Exception as e:
            print e
            raise e

    def test_university_of_saskatchewan(self):
        line = '|coordinates = |52|8|12|N|106|37|51|W|\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 52.13666666666666)
        self.assertEqual(coordinates['longitude'], -106.63083333333333)

    def test_dahlonega(self):
        line = "{{Coord|34.5299|-83.9871|display=title}}The '''Dahlonega Mint''' was a former [[Branch mint|branch]] of the [[United States Mint]] built during the [[Georgia Gold Rush]] to help the miners get their gold [[assayed]] and [[coining (mint)|minted]], without having to travel to the [[Philadelphia Mint]].&lt;ref name=Williams/&gt;{{rp|80\xe2\x80\x9381,105}}  It was located at (34\xc2\xb031.8\xe2\x80\xb2N 83\xc2\xb059.2\xe2\x80\xb2W ) in [[Dahlonega]], [[Lumpkin County, Georgia]]. Coins produced at the Dahlonega Mint bear the &quot;D&quot; [[mint mark]]. That mint mark is used today by the [[Denver Mint]], which opened many years after the Dahlonega Mint closed. All coins from the Dahlonega Mint are gold, in the $1, $2.50, $3, and $5 denominations, and bear dates in the range 1838\xe2\x80\x931861.\n"
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 34.5299)
        self.assertEqual(coordinates['longitude'], -83.9871)


    def test_fort_oglethorpe(self):
        line = """'|coordinates = 34\xc2\xb056\xe2\x80\xb258.75\xe2\x80\xb3N 85\xc2\xb015\xe2\x80\xb210.66\xe2\x80\xb3W\n'"""
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 34.94965277777777)
        self.assertEqual(coordinates['longitude'], -85.2529611111111)

    def test_cut_knife(self):
        line = """'{{Coord|display=title|name=Cut Knife, Saskatchewan|52|45|N|109|01|W|region:CA_type:city}}\n'"""
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 52.75)
        self.assertEqual(coordinates['longitude'], -109.01666666666667)

    def test_new_south_wales(self):
        line = '|coordinates = {{coord|32|S|147|E}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], -32)
        self.assertEqual(coordinates['longitude'], 147)

    def test_st_johns(self):
        # does the name have to match the name of the page, i.e. title??
        # should they be able to pass in the name??
        line = '{{Coord|display=title|name=Truro|43|38|23|N|79|25|57.3|W|type:landmark_region:CA-ON}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 43.63972222222222)
        self.assertEqual(coordinates['longitude'], -79.43258333333334)

    def test_fort_hunter(self):
        line = '|coordinates = {{coord|35.952226|N|121.23065|W}}&lt;ref&gt;{{gnis|2512470|Fort Hunter Liggett}}&lt;/ref&gt;\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 35.952226)
        self.assertEqual(coordinates['longitude'], -121.23065)

    def test_peyto_glacier(self):
        line = '{{Coord|display=title|name=Peyto Glacier|51|40|41|N|116|32|50|W|region:CA_type:glacier_source:GNS-enwiki}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 51.67805555555555)
        self.assertEqual(coordinates['longitude'], -116.54722222222222)

    def test_achill_island(self):
        line = '| coordinates = {{coords|53.96391|-10.00303|display=it}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 53.96391)
        self.assertEqual(coordinates['longitude'], -10.00303)

    def test_church_street(self):
        line = '| coordinates = {{coord|  51.8128|-2.7147 |display=inline,title}}\n'
        coordinates = extract_coordinates(line, debug=False)
        self.assertEqual(coordinates['latitude'], 51.8128)
        self.assertEqual(coordinates['longitude'], -2.7147)




if __name__ == '__main__':
    unittest.main()
