import os
import re
import urllib2
import sys
import json
import time


pair='XXBTZEUR'

opener = urllib2.build_opener()
#User Agent Has To be Set To something Other Than Default
opener.addheaders = [('User-agent', 'MIT IS THE BEST')]


response = opener.open("https://api.kraken.com/0/public/Depth?pair="+pair)
order_book=json.load(response)['result'][pair]
krkn_asks = [[str(x[0]).replace('"',''),str(x[1]).replace('"','')] for x in order_book['asks']]
krkn_bids = [[str(x[0]).replace('"',''),str(x[1]).replace('"','')] for x in order_book['bids']]

print krkn_bids
print krkn_asks
