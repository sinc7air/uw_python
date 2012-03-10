import math
import json
import pprint
import urllib2
import datetime

class ISSPASS:
  def __init__(self,RISETIME = 0, DURATION = 0):
    self.RISETIME = RISETIME
    self.DURATION = DURATION
  def niceRise(self):
    return datetime.datetime.fromtimestamp(self.RISETIME)
  def niceDuration(self):
    return '%s Min %s Sec' % (int(math.floor(self.DURATION / 60)), self.DURATION%60)

def getISSPasses(LAT=47.608792, LONG=-122.345755, ALT=4, N=1):
  passes=urllib2.urlopen('http://api.open-notify.org/iss/?lat=%s&lon=%s&alt=%s&n=%s' % (LAT, LONG, ALT, N))
  passes_json = json.load(passes)
  ISS = ISSPASS(RISETIME = passes_json['response'][0]['risetime'], DURATION = passes_json['response'][0]['duration'])
  return ISS
  
def getISSPosition():
  position_raw = urllib2.urlopen('http://api.open-notify.org/iss-now/')
  position = json.load(position_raw)
  return [position['iss_position']['latitude'],position['iss_position']['longitude']]


