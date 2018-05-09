import requests
import time
import signal
import sys


def main() :

	while True :
		print( 'Press Ctrl+C To Stop Demo\n' )
		userName = str( input("Please Type User's Name To Get Data: ") )
		contractAddress, contractABI, userToken = getDataFromGovernment( userName )
		# print( contractAddress )
		# print( contractABI )
		# print( userToken )
		getContract( contractAddress, contractABI )
		time.sleep(0.5)
	

def getDataFromGovernment( userName ) :
	
	link = 'http://localhost:5000/contract'
	res = requests.post( link, { 'name': userName })

	if res.status_code == 201 :
		res = res.json()

	else :
		return None, None, None

	return res['contractAddress'], res['contractABI'], res['userToken']



def getContract( contractAddress, contractABI ) :

	from web3 import Web3, HTTPProvider, contract
	from solc import compile_source, compile_files, link_code
	
	web3 = Web3( HTTPProvider( 'http://localhost:8545' ) )
	eth = web3.eth
	assert web3.isConnected()
	assert eth.accounts

	ID_Recognition_Contract = eth.contract( address=contractAddress, )
	print( ID_Recognition_Contract.address )
	print( ID_Recognition_Contract.abi )
	pass


def signal_handler(signal, frame):
    print ('\nExit By Keyboad! Bye!' )
    sys.exit(0)


if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)

	main()
	
	signal.pause()
