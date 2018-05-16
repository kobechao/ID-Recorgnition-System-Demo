/**
 * The contractName contract does this and that...
 */

pragma solidity ^0.4.8;

contract ID_Recognition {

	mapping (bytes32 => bool) userRegisterTable;

	event LogRegisterIsSuccessed(address sender, bool isSuccessed, string msg);
	event LogGetRegisterData(address sender, bool isSuccessed, string msg);
	

	address admin;
	
	function ID_Recognition () {
		admin = msg.sender;
	}	

	modifier isAdmin() { 
		require ( msg.sender == admin ); 
		_; 
	}

	function setUserRegisterTable ( string userID ) isAdmin returns(bool res)  {
		bool successed = false;
		if( !isUserRegistered( userID ) ) {
			userRegisterTable[ sha256(userID) ] = true;
			successed = true;
		} else {
			successed = false;
		}

		LogRegisterIsSuccessed( msg.sender, successed, "" );
		return successed;
 	}


	function getUserRegisterTable ( string userID ) constant returns(bool isRegistered)  {
		LogGetRegisterData( msg.sender, isUserRegistered( userID ), "" );
		return userRegisterTable[ sha256(userID) ];
	}


	function isUserRegistered ( string userID ) isAdmin constant returns(bool isRegistered)  {
		return userRegisterTable[ sha256(userID) ] == true;
	}
	
}
