import urllib2
import json
f = urllib2.urlopen('http://api.wunderground.com/api/0def10027afaebb7/conditions/q/WA/EVERETT.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = "Everett, WA" 
temp_f = parsed_json['current_observation']['temp_f']
wind_speed = parsed_json['current_observation']['wind_mph']
print "Current temperature in %s is: %s Degrees F" % (location, temp_f)
print "Current wind speed in %s is: %s mph" % (location, wind_speed)
f.close()
