class ApiExecuter():
	"""
	"""
	def __init__(self, url, contractData, insertData=None):
		self.url = url
		assert type(contractData) == dict
		self.contractData = contractData
		self.insertData = insertData
		self.postData = { **self.contractData, **self.insertData } if self.insertData else self.contractData


	def getDBRespondData( self ):
		import requests
		res = requests.post( self.url, self.postData )
		print( res.json() )
		print()

		return res.json()






		