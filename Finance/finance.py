import requests
import time
import signal
import sys


def main() :

	while True :
		print( 'Press Ctrl+C To Stop Demo\n' )
		userName = str( input("Please Type User's Name To Get Data: ") )
		contractAddress, contractABI, userToken = getDataFromGovernment( userName )
		if all( [contractAddress, contractABI, userToken] ) :
			ID_Recognition_Contract = getContract( contractAddress, contractABI )
			test( ID_Recognition_Contract )
		else:
			print( 'No Such User' )

		time.sleep(0.5)
	

# =====================================
def getDataFromGovernment( userName ) :
	
	link = 'http://localhost:5000/contract'
	res = requests.post( link, { 'name': userName })

	if res.status_code == 201 :
		res = res.json()

	else :
		return None, None, None

	return res['contractAddress'], res['contractABI'], res['userToken']


# ===============================================
def getContract( contractAddress, contractABI ) :

	from web3 import Web3, HTTPProvider, contract
	from web3.contract import ConciseContract
	import json
	
	web3 = Web3( HTTPProvider( 'http://localhost:8545' ) )
	eth = web3.eth
	assert web3.isConnected()
	assert eth.accounts
	contractABI = eval(contractABI) 

	ID_Recognition_Contract = eth.contract( address=contractAddress, abi=contractABI, ContractFactoryClass=ConciseContract )
	# _tx = ID_Recognition_Contract.getUserRegisterTable( "kobe" )

	return ID_Recognition_Contract

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
