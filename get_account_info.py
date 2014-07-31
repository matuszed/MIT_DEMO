import json
import time
import time,hmac,base64,hashlib,urllib,urllib2,json
from hashlib import sha256
from decimal import Decimal

class kraken:
	timeout = 15
	tryout = 0

	def __init__(self, key='', secret='', agent='Kraken PHP API Agent'):
		self.key, self.secret, self.agent = key, secret, agent
		self.time = {'init': time.time(), 'req': time.time()}
		self.reqs = {'max': 10, 'window': 10, 'curr': 0}
		self.base = 'https://api.kraken.com'

	def throttle(self):
		# check that in a given time window (10 seconds),
		# no more than a maximum number of requests (10)
		# have been sent, otherwise sleep for a bit
		diff = time.time() - self.time['req']
		if diff > self.reqs['window']:
			self.reqs['curr'] = 0
			self.time['req'] = time.time()
		self.reqs['curr'] += 1
		if self.reqs['curr'] > self.reqs['max']:
			print 'Request limit reached...'
			time.sleep(self.reqs['window'] - diff)

	def makereq(self, path, data , nonce):

		# bare-bones hmac rest sign
		sign=str(hmac.new(base64.b64decode(self.secret), path +
				  sha256(nonce+data).digest()
				  , hashlib.sha512).digest())
		return urllib2.Request(self.base + path, data, {
			'User-Agent': self.agent,
			'API-Key: ': self.key,
			'API-Sign: ': base64.b64encode(sign)
		})

	def req(self, path, inp={}):
		t0 = time.time()
		tries = 0
		while True:
			# check if have been making too many requests
			self.throttle()

			try:
				# send request to mtgox
				n=str(int(time.time() * 1e6))
				inp['nonce'] = n
				inpstr = urllib.urlencode(inp.items())
				req = self.makereq(path, inpstr,n)
				response = urllib2.urlopen(req, inpstr)

				# interpret json response
				output = json.load(response)
				if 'error' in output:
					if output['error']!=[]:
						print output
						raise ValueError(output['error'])


				return output['result']

			except Exception as e:
				print "Error: %s" % e

			# don't wait too long
			tries += 1
			if time.time() - t0 > self.timeout or tries > self.tryout:
				raise Exception('Timeout')                              


api_version="/0/"
krak = kraken('','')
balances=krak.req(api_version+'private/Balance',{})

for item in balances:
	print item+" : "+balances[item]
