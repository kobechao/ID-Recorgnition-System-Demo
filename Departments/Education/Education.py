from flask import Flask, abort, jsonify, request

from web3 import Web3, HTTPProvider, contract
from web3.contract import ConciseContract
	
web3 = Web3( HTTPProvider( 'http://localhost:8545' ) )
eth = web3.eth
assert web3.isConnected()
assert eth.accounts

import json
import requests
import pymysql


app = Flask(__name__)


@app.route('/api/EducationData', methods=['POST'] )
def BankData() :
	if request.method == 'POST' :
		form = request.form
		# print( form )

		personalID = form.get( 'personalID', None )
		userToken = form.get( 'userToken', None )
		contractAddress = form.get( 'contractAddress', None )
		contractABI = form.get( 'contractABI', None)

		if all( [personalID, userToken, contractAddress, contractABI] ) :
			if all( isValidUser( personalID, userToken, contractAddress, contractABI ) ):
				userData = getData( personalID )
				return jsonify( userData )

		else :
			return jsonify( { 'error': 'Not Found' } )

		return False

	else :
		abort(404)


def isValidUser( personalID, userToken, contractAddress, contractABI ) :

	contractABI = eval(contractABI) 
	ID_Recognition_Contract = eth.contract( address=contractAddress, abi=contractABI, ContractFactoryClass=ConciseContract )
	
	print( 'Checking Contract %s Is Deployed By Government...' % contractAddress)	
	
	governmentAddr = eth.accounts[0]
	isValidGovernment = eth.getTransaction( userToken ).get('from') == governmentAddr

	print( 'isValidGovernment: ' + str( isValidGovernment ) + '\n' )

	print( 'Checking The User Is Registered In Contract By Token %s, ID %s...' % ( userToken, personalID ) )	
	
	isValidUser = ID_Recognition_Contract.getUserRegisterTable( personalID )

	print( 'isValidUser: ' + str( isValidUser ) + '\n' )


	return isValidGovernment, isValidUser


def getData( personalID ):
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	cursor = conn.cursor()

	sql = 'SELECT * FROM education_data WHERE personalID=\'%s\''
	print( sql )
	cursor.execute( sql % personalID )
	data = cursor.fetchone()

	if data :
		return dict({
				'userName': data[1],
				'personalID': data[2],
				'birthday': data[3],
				'schoolName': data[4], 
				'department': data[5],
				'grade': data[6],
			})
	else :
		return dict({
				'error': 'No Such User',
			})


if __name__ == '__main__':
	app.run( port=8002, debug=True )


