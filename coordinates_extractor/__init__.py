from re import IGNORECASE, search

patterns = {
    "direction": "(?P<direction>[NWSE])",
    "number": "-?\d{1,3}(?:\.\d{1,8})?",
    "degrees": "(?P<degrees>\d{1,3}(?:\.\d{1,8})?)",
    "minutes": "(?P<minutes>\d+)",
    "seconds": "(?P<seconds>\d{1,3}(?:\.\d{1,8})?)"
}

for key, pattern in patterns.items():
    if pattern.startswith("(?P<"):
        for n in range(1, 3):
            patterns[key + str(n)] = pattern.replace(key, key + str(n))

#print "patterns:", patterns
    

#http://stackoverflow.com/questions/33997361/how-to-convert-degree-minute-second-to-degree-decimal-in-python
def dms2dd(degrees, minutes, seconds, direction, debug=False):
    if debug: print "[coordinates-extractor] starting dms2dd with", [degrees, minutes, seconds, direction, debug]
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction in ("S", "W"):
        dd *= -1
 
    if debug: print "[coordinates-extractor] finishing dms2dd with", dd
    return dd;


def extract_coordinates_from_line(line, debug=False):

    try:

        if debug: print "[coordinates-extractor] starting extract_coordinates_from_line with", line

        result = {}

        splat = line.split("|")
        if debug: print "[coordinates-extractor]: splat is", splat
        if (("N" in splat) + ("S" in splat) + ("E" in splat) + ("W" in splat)) == 2:
            if debug: print "[coordinates-extractor]: at least 2 of the following are in the line: N, S, W, and E"
            search_pattern = "{{coord\| ?" + patterns['degrees1'] + " ?(?:\| ?" + patterns['minutes1'] + " ?)? ?(?:\| ?" + patterns['seconds1'] + " ?)?\| ?" + patterns['direction1'] + " ?\| ?" + patterns['degrees2'] + " ?(?:\| ?" + patterns['minutes2'] + " ?)?(?:\| ?" + patterns['seconds2'] + " ?)?\| ?" + patterns['direction2']
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
                if "latd" in d:
                    result['latitude'] = dms2dd(d["latd"], d.get("latm", 0), d.get("lats", 0), "N")
                if "longd" in d:
                    result['longitude'] = dms2dd(d["longd"], d.get("longm", 0), d.get("longs", 0), "N")
 
        else:
            mg = search("{{Coord\|(?P<latitude>" + patterns['number'] + ")\|(?P<longitude>" + patterns['number'] + ")", line, IGNORECASE)
            if mg:
                groupdict = mg.groupdict()
                if debug: print "[coordinates-extractor]: groupdict is", groupdict 
                if "latitude" in groupdict and "longitude" in groupdict:
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
            temp_result = extract_coordinates_from_line(element)
            for key in ["latitude", "longitude"]:
                if key not in result and key in temp_result:
                    result[key] = temp_result[key]

        return result

    except Exception as e:

        print "[coordinates-extractor.extract_first_coordinate_pair_from_list]:", e

def extract_coordinates(line, debug=False):
    return extract_coordinates_from_line(line, debug=debug)

