import requests
import time
import signal
import sys


# ==========
def main() :

	while True :
		print( 'Press Ctrl+C To Stop Demo\n' )
		userName = str( input("Please Type User's Name To Get Data: ") )
		contractAddress, contractABI, userToken = getContractDataFromGovernment( userName )
		if all( [contractAddress, contractABI, userToken] ) :
			ID_Recognition_Contract = getContract( contractAddress, contractABI, userToken )
			# test( ID_Recognition_Contract )
			# getContractDataFromGovernment( userName, userToken )
		else:
			print( 'No Such User' )

		time.sleep(0.5)
	

# =============================================
def getContractDataFromGovernment( userName ) :
	
	link = 'http://localhost:5000/api/contract'
	res = requests.post( link, { 'name': userName })

	if res.status_code == 201 :
		res = res.json()

	else :
		return None, None, None

	return res['contractAddress'], res['contractABI'], res['userToken']


# =============================================
def getPersonalDataFromGovernmnet( userToken ) :
	
	link = 'http://localhost:5000/api/userdata'
	res = requests.post( link, { 'token': userToken })
	

	if res.status_code == 201 :
		res = res.json()
		return True, res
	else :
		print ( res )
		return False, res.status_code


# ===============================================
def getContract( contractAddress, contractABI, userToken ) :

	from web3 import Web3, HTTPProvider, contract
	from web3.contract import ConciseContract
	import json
	
	web3 = Web3( HTTPProvider( 'http://localhost:8545' ) )
	eth = web3.eth
	assert web3.isConnected()
	assert eth.accounts

	contractABI = eval(contractABI) 
	ID_Recognition_Contract = eth.contract( address=contractAddress, abi=contractABI, ContractFactoryClass=ConciseContract )

	governmentAddr = eth.accounts[0]
	isValid = eth.getTransaction( userToken ).get('from') == governmentAddr

	print( isValid )
	if isValid :
		res = getPersonalDataFromGovernmnet( userToken )
		return res, isValid
	else :
		print( 'illegal' )
		return None, isValid


# ================================
def signal_handler(signal, frame):
    print ('\nExit By Keyboad! Bye!' )
    sys.exit(0)


# ==================================
def test( ID_Recognition_Contract) :
	for testName in ['kobe','tina', 'cindy', 'hao', 'lulu'] :
		print( testName + '\t' + str(ID_Recognition_Contract.getUserRegisterTable( testName ) ))


if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)

	main()
	
	signal.pause()
