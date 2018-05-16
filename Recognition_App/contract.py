# -*- coding: UTF-8 -*-

'''
ID_Recognition. Contract
Using web3.py to communicate with the whole new contract
@ edition: 1
'''
from web3 import Web3, HTTPProvider, contract
from solc import compile_source, compile_files, link_code
import os

web3 = Web3( HTTPProvider( 'http://localhost:8545' ) )
eth = web3.eth
assert web3.isConnected()
assert eth.accounts

class ID_Recognition_Contract():

	"""IDStorage_contract class in python"""

	def __init__( self ):
		self.governmentAddr = eth.accounts[0]
		self.contractBytecode, self.contractABI = self.get_Bytecode_ABI()
		self.contract_Recognition = eth.contract( abi = self.contractABI, bytecode = self.contractBytecode )
		self.contractHash = self.contract_Recognition.deploy( transaction = { "from": self.governmentAddr } )
		self.receipt = eth.getTransactionReceipt( self.contractHash )
		self.address = self.receipt.get('contractAddress', None)

		print( '\nContract Deployed at\n%s\n%s\n' % ( self.address, '=' * len( self.address ) ) )

	def get_Bytecode_ABI( self ) :
		contractPath = ['Recognition_App/contract/ID_Recognition.sol']
		compiledValues = list(compile_files( contractPath ).values())[0]
		return compiledValues['bin'] ,compiledValues['abi']


	def setUserRegisterTable( self, userID ) :
		_tx = self.contract_Recognition.transact( { 'from': self.governmentAddr, 'to': self.receipt['contractAddress'] } ).setUserRegisterTable( userID )
		return _tx


	def getUserRegisterTable( self, userID ) :
		_tx = self.contract_Recognition.call( {  'to': self.receipt['contractAddress'] } ).getUserRegisterTable( userID )
		return _tx


	def getTx( self, tx ) :
		_tx = eth.getTransaction( tx )
		return _tx


def getContractDBData( personalID ):

	import pymysql
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	cursor = conn.cursor()

	sql = 'SELECT personalID, contractAddress, contractABI, userToken FROM contract_data WHERE personalID=\'%s\';'
	cursor.execute( sql % personalID )

	userData = cursor.fetchone()

	cursor.close()
	conn.close()

	if userData :
		return dict({
			'personalID': userData[0],
			'contractAddress': userData[1],
			'contractABI': userData[2],
			'userToken': userData[3],
		})

	else :
		return None



if __name__ == '__main__':

	# test()
	contract = ID_Recognition_Contract()
	tx = contract.setUserRegisterTable('123')
	print( type(tx), len(tx.hex()) )
	print( 'rawTx: ', web3.sha3( tx ))
	print ( '123: ', contract.getUserRegisterTable('123'))
	print ( 'receipt: ', contract.getTx(tx) )




