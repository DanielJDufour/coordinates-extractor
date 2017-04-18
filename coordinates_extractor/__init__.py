from re import IGNORECASE, search

patterns = {
    "comment": "(?:&lt;!--\d+--&gt;)?",
    "deg": "(?P<deg>\d{1,3}(?:\.\d{1,15})?)\xc2\xb0",
    "min": "(?P<min>\d{1,3}(?:\.\d{1,15})?)('|\xe2\x80\xb2)",
    "sec": "(?P<sec>\d{1,3}(?:\.\d{1,15})?)(\"|\xe2\x80\xb3)",
    "direction": "(?P<direction>[NWSE])",
    "ignore": "(?:\|display ?= ?title)?(?:\|name ?= ?[A-Z ,]*)?",
    "number": "-?\d{1,3}(?:\.\d{1,15})?",
    "degrees": "(?P<degrees>\d{1,3}(?:\.\d{1,15})?)",
    "minutes": "(?P<minutes>\d+)",
    "seconds": "(?P<seconds>\d{1,3}(?:\.\d{1,15})?)"
}

for key, pattern in patterns.items():
    if pattern.startswith("(?P<"):
        for n in range(1, 3):
            patterns[key + str(n)] = pattern.replace(key, key + str(n))

#print "patterns:", patterns
    

#http://stackoverflow.com/questions/33997361/how-to-convert-degree-minute-second-to-degree-decimal-in-python
def dms2dd(degrees, minutes, seconds, direction, debug=False):

    try:

        if debug: print "[coordinates-extractor] starting dms2dd with", [degrees, minutes, seconds, direction, debug]
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
        if direction in ("S", "W"):
            dd *= -1
 
        if debug: print "[coordinates-extractor] finishing dms2dd with", dd
        return dd;

    except Exception as e:

        if debug: print "[coordinates-extractor.dms2dd] caught exception", e


def extract_coordinates_from_line(line, debug=False):

    try:

        if debug: print "[coordinates-extractor] starting extract_coordinates_from_line with", line

        result = {}

        found_at = None


        # we do the replace in the line below to handle the case where the
        # direction comes at the end of the tag like
        # {{coord|35.952226|N|121.23065|W}}
        splat = [part.strip() for part in line.replace("}}","|}}").split("|")]
        if debug: print "[coordinates-extractor]: splat is", splat
        if (("N" in splat) + ("S" in splat) + ("E" in splat) + ("W" in splat)) == 2:
            if debug: print "[coordinates-extractor]: at least 2 of the following are in the line: N, S, W, and E"
            search_pattern = "(?:{{coord|coordinates ?=) ?" + patterns['ignore']  + "\| ?" + patterns['degrees1'] + " ?(?:\| ?" + patterns['minutes1'] + " ?)? ?(?:\| ?" + patterns['seconds1'] + " ?)?\| ?" + patterns['direction1'] + " ?\| ?" + patterns['degrees2'] + " ?(?:\| ?" + patterns['minutes2'] + " ?)?(?:\| ?" + patterns['seconds2'] + " ?)?\| ?" + patterns['direction2']
            if debug: print "[coordinates-extractor]: search_pattern is", search_pattern
            mg = search(search_pattern, line, IGNORECASE)
            if mg:
                groupdict = mg.groupdict()
                if debug: print "[coordinates-extractor]: groupdict is", groupdict 
                if all(key in groupdict for key in ["degrees1", "direction1", "degrees2", "direction2"]):
                    for i in ['1','2']:
                        if debug: print "[coordinates-extractor]: i = ", i
                        direction = groupdict['direction' + i]
                        if debug: print "\t[coordinates-extractor]: direction: ", i
                        value = dms2dd(groupdict['degrees'+i], groupdict['minutes'+i] or 0, groupdict['seconds'+i] or 0, direction, debug=debug)
                        if debug: print "\t[coordinates-extractor]: value: ", value
                        if direction in ("N", "S"):
                            result['latitude'] = value
                        elif direction in ("W", "E"):
                            result['longitude'] = value

        elif line.startswith("| latd") or line.startswith("| longd"):
            if debug: print "[coordinates-extractor]: line starts with | latd or | longd"

            # converts '| latd  = 34  | latm  = 55 | lats  = 44.4\n'
            # to {'latm': '55', 'latd': '34', 'lats': '44.4'}
            d = dict([[b.strip() for b in a.split("=")] for a in line.split("|") if a])
            if debug: print "[coordinates-extractor]: d is", d
            if d:
                if "latd" in d or "latd1" in d or "latd2" in d:
                    latd = d.get("latd", None) or d.get("latd1", None) or d.get("latd2", None)
                    latm = d.get("latm", None) or d.get("latm1", None) or d.get("latm2", None) or 0
                    lats = d.get("lats", None) or d.get("lats1", None) or d.get("lats2", None) or 0
                    result['latitude'] = dms2dd(latd, latm, lats, "N")
                if "longd" in d or "longd1" in d or "longd2" in d:
                    longd = d.get("longd", None) or d.get("longd1", None) or d.get("longd2", None)
                    longm = d.get("longm", None) or d.get("longm1", None) or d.get("longm2", None) or 0
                    longs = d.get("longs", None) or d.get("longs1", None) or d.get("longs2", None) or 0
                    result['longitude'] = dms2dd(longd, longm, longs, "N")
 
        elif "\xc2\xb0" in line:
            if debug: print "[coordinates-extractor]: \xc2\xb0 in line"
            search_pattern = patterns['deg1'] +  " ?(?:" + patterns['min1'] + ")? ?(?:" + patterns['sec1'] + ")? ?" + patterns['direction1'] + " " + patterns['deg2'] + " ?(?:" + patterns['min2'] + ")? ?(?:" + patterns['sec2'] + ")? ?" + patterns['direction2']
            if debug: print "[coordinates-extractor]: search_pattern is", search_pattern
            mg = search(search_pattern, line, IGNORECASE)
            if debug: print "[coordinates-extractor]: mg is", mg
            if mg:
                groupdict = mg.groupdict()
                if debug: print "[coordinates-extractor]: groupdict is", groupdict 
                if all(key in groupdict for key in ["deg1", "direction1", "deg2", "direction2"]):
                    for i in ['1','2']:
                        if debug: print "[coordinates-extractor]: i = ", i
                        direction = groupdict['direction' + i]
                        if debug: print "\t[coordinates-extractor]: direction: ", i
                        value = dms2dd(groupdict['deg'+i], groupdict['min'+i] or 0, groupdict['sec'+i] or 0, direction, debug=debug)
                        if debug: print "\t[coordinates-extractor]: value: ", value
                        if direction in ("N", "S"):
                            result['latitude'] = value
                        elif direction in ("W", "E"):
                            result['longitude'] = value
                        found_at = mg.start()
                        if debug: print "found_at:", found_at

        # don't do elif beause sometimes have degree sign appearing in text 
        if not result or found_at > 300:
            pattern = "{{Coords? ?" + patterns['ignore']  + "?\| ?(?P<latitude>" + patterns['number'] + " ?)" + patterns['comment'] + " ?\| ?(?P<longitude>" + patterns['number'] + " ?)" + patterns['comment'] + " ?"
            if debug: print "pattern:", [pattern]
            mg = search(pattern, line, IGNORECASE)
            if mg:
                if debug: print "found at:", mg.start()
                groupdict = mg.groupdict()
                if debug: print "[coordinates-extractor]: groupdict is", groupdict 
                if (found_at is None or found_at - mg.start() > 300) and "latitude" in groupdict and "longitude" in groupdict:
                    result['latitude'] = float(groupdict['latitude'])
                    result['longitude'] = float(groupdict['longitude'])
 
        if debug: print "[coordinates-extractor]: finishing extract_coordinates_from_line with", result 

        return result

    except Exception as e:

        print "[coordinates-extractor]:", e

# tries to get lat and long and returns when have both
def extract_first_coordinate_pair_from_list(lst, debug=False):

    try:
        result = {}
        for element in lst:
            temp_result = extract_coordinates_from_line(element, debug=debug)
            for key in ["latitude", "longitude"]:
                if key not in result and key in temp_result:
                    result[key] = temp_result[key]

        return result

    except Exception as e:

        print "[coordinates-extractor.extract_first_coordinate_pair_from_list]:", e

def extract_coordinates(line, debug=False):
    return extract_coordinates_from_line(line, debug=debug)

