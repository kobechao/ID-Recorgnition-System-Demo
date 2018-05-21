class ApiExecuter():
	"""
	"""
	def __init__(self, url, postdata):
		self.url = url
		assert type(postdata) == dict
		self.postdata = postdata
		self.respondData = self.getDBData()

	def getDBData( self ):
		import requests

		res = requests.post( self.url, {
				'personalID': self.postdata['personalID'],
				'userToken': self.postdata['userToken'],
				'contractAddress': self.postdata['contractAddress'],
				'contractABI': self.postdata['contractABI']
			})

		print( res.json() )
		print( '=' * len( str(res.json()) ) )

		return res.json()

	def getRespondData( self ):
		return self.respondData





		