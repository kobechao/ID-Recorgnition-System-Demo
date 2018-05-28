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


@app.route('/api/BankData/<url_implement>', methods=['POST'] )
def BankData( url_implement ) :
	# print( url_implement )
	if request.method == 'POST' :
		form = request.form

		# print( form )

		personalID = form.get( 'personalID', None )
		userToken = form.get( 'userToken', None )
		contractAddress = form.get( 'contractAddress', None )
		contractABI = form.get( 'contractABI', None)
		
		assert all( [personalID, userToken, contractAddress, contractABI] )

		if all( isValidUser( personalID, userToken, contractAddress, contractABI ) ):
			val = form.get( 'value', None )

			if url_implement == 'getUserData' :
				userData = getData( personalID )
				return jsonify( userData )

			elif url_implement == 'insertUserData' :
				userName = form.get( 'name', None )
				birthday = form.get( 'birthday', None )
				bankAccount = form.get( 'bankAccount', None )
				amount = form.get( 'amount', None )

				insertData( personalID, userName, birthday, bankAccount, amount )
				return jsonify( {'BANK': 'test'} )

			else :
				return jsonify( { 'error': 'error' } )

		else:
			abort(404)


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

	sql = 'SELECT * FROM finance_data WHERE personalID=\'%s\''
	cursor.execute( sql % personalID )
	data = cursor.fetchone()

	if data :
		return dict({
				'userName': data[1],
				'personalID': data[2],
				'birthday': data[3],
				'bankAccount': data[4], 
				'amount': data[5],
			})

		return dict({
				'error': 'No Such User',
			})

def insertData( personalID, userName, birthday, bankAccount, amount ):
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	cursor = conn.cursor()

	try :
		sql = "INSERT INTO finance_data (userName, personalID, birthday, bankAccount, amount) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"
		cursor.execute( sql % ( userName, personalID, birthday, bankAccount, amount ) )

		conn.commit()

	except Exception as e :
		print( e )

	finally:
		cursor.close()
		conn.close()
		return True


if __name__ == '__main__':
	app.run( port=8001, debug=True )