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


@app.route('/api/BankData', methods=['POST'] )
def BankData() :
	if request.method == 'POST' :
		form = request.form
		# print( form )

		personalID = form.get( 'personalID', None )
		userToken = form.get( 'userToken', None )
		contractAddress = form.get( 'contractAddress', None )
		contractABI = form.get( 'contractABI', None)

		if all( [personalID, userToken, contractAddress, contractABI] ) :
			if isValidUser( personalID, userToken, contractAddress, contractABI ) :
				userData = getData( personalID )
				return jsonify( userData )

		else :
			pass

		return False

	else :
		abort(404)


def isValidUser( personalID, userToken, contractAddress, contractABI ) :

	contractABI = eval(contractABI) 
	ID_Recognition_Contract = eth.contract( address=contractAddress, abi=contractABI, ContractFactoryClass=ConciseContract )
	
	print( 'Checking Validity From Contract...')
	
	governmentAddr = eth.accounts[0]
	isValid = eth.getTransaction( userToken ).get('from') == governmentAddr

	print( 'Validity: ' + str( isValid ) )

	return isValid


def getData( personalID ):
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	cursor = conn.cursor()

	sql = 'SELECT * FROM finance_data WHERE personalID=\'%s\''
	print( sql )
	cursor.execute( sql % personalID )
	data = cursor.fetchone()

	if data :
		return dict({
				'userName': data[1],
				'personalID': data[2],
				'birthday': data[3],
				'bankAccount': data[4], 
				'amount': data[5],
			}), 201
	else :
		return dict({
				'error': 'No Such User',
			}), 400

if __name__ == '__main__':
	app.run( port=8001, debug=True )