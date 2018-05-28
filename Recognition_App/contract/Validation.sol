pragma solidity ^0.4.8;

contract Validation {

    // within node address, and BU name
    struct BU {
        string buName;
        uint256 buCode;
        uint8 permissionCode;
    }


    // BU data manipulations
    uint8 BU_Count;
    mapping( address => BU ) BU_Mapping;
    mapping( uint => BU ) BU_Code_Mapping;
    address[] BU_Address_List;


    // User data manipulations
    mapping( bytes32 => uint256 ) buTable;
    mapping( bytes32 => uint256 ) permissionTable;


    // permission arguments, seldom modify
    uint8 constant CanInitBU = 8;
    uint8 constant CanSetPermission = 4;

    uint8 constant CanModifyBU = 2;
    uint8 constant CanGetPermission = 1;


    // timeout
    int constant PermissionTimeOut = 15;


    // administrator's address
    address admin;


    // function events
    event LogInitBU( bytes32 idHash, bool isSuccessed );
    event LogGetBU( bytes32 idHash, bool isSuccessed, address addr );
    event LogModifyBU( bytes32 idHash, address addr );
    event LogRegisterBU( string buCode, bool isSuccessed );

    event LogSetPermission( bytes32 idHash, bool isSuccessed );
    event LogGetPermissionTimeValid( bytes32 idHash );
    event LogGetPermissionTimeExpired( bytes32 idHash );


    // constructor
    function Validation ( ) {
        admin = msg.sender;
        BU_Count = 0;
    }


    // modifier
    modifier isAdmin() {
        if( msg.sender != admin ) {
            throw;
        }
        _;
    }


    // BU register
    function BU_register( string name, address bu_addr ) {

        if( getBUCode( bu_addr ) != 0 ) {
            LogRegisterBU( name, false );
            return;
        }

        uint BUCode = 1 << BU_Count;

        BU_Mapping[bu_addr] = BU ({
            buName: name,
            buCode: BUCode,
            permissionCode: 15
        });
        BU_Code_Mapping[BUCode] = BU ({
            buName: name,
            buCode: BUCode,
            permissionCode: 15
        });
        BU_Count ++ ;
        LogRegisterBU( name, true );
    }


    // how many BUs registere to the chain
    function getCount() isAdmin constant returns( uint ){
        return BU_Count;
    }

    // get BU code
    function getBUCode( address bu_addr ) constant returns( uint256 ) {
        return BU_Mapping[ bu_addr ].buCode;
    }
    


    // Get all avaliable BU
    function getAvailableBU() constant returns ( uint ) {
        return( 2**BU_Count - 1 );
    }


    // check which BU the user can access
    function userGetAccessedBU( string IDNumber ) isAdmin constant returns( uint256[] ) {
        uint256[] storage accessedList;
        uint256 userBUCode = buTable[ sha256(IDNumber) ];
        for( uint8 i=0; i<BU_Count; i++ ) {
            uint8 comp = 1 << i;
            if( ( userBUCode & comp ) > 0 ) {
                accessedList[BU_Count-i-1]=comp ;
            }
        }

        return accessedList;
    }


   // [test] get accessed BU string
    function userGetBUString( address bu_addr ) constant returns( string ) {    
        return BU_Mapping[bu_addr].buName ;
    
    }

    // initialize buTable with integer 0
    function userInitBUTable( string IDNumber, address bu_addr ) returns( bool ) {

        bytes32 regID = sha256( IDNumber );
        if( buTable[regID] == 0 && getBUCode( bu_addr ) != 0 ) {
            buTable[regID] = BU_Mapping[ bu_addr ].buCode;

            LogInitBU( regID, true );
            return true;
        }
        
        LogInitBU( regID, false );
        return false;
    }


    // [test] set user BU table
    function userSetBUTable ( string IDNumber, address bu_addr )  {

        bytes32 idhash = sha256(IDNumber);
        uint256 bus = buTable[ idhash ] ;
        uint256 code = BU_Mapping[ msg.sender ].buCode;
        
        if ( (bus & code == 0) && getBUCode( bu_addr ) != 0 ){
            buTable[ idhash ] = bus + code;
        }

    }


    // get the user's BU table
    function userGetBUTable( string IDNumber ) isAdmin constant returns( uint256 ) {
        return buTable[ sha256(IDNumber) ];
    }


    // verified
    function userGetVerifiedBU( string IDNumber ) returns ( uint256 ) {
        return 0;
    }
    

    // single-sign-on server only, which set now time to permissionTable
    function setPermission( string IDNumber ) public isAdmin returns( uint256 ) {
        LogSetPermission( sha256(IDNumber), true );
        permissionTable[ sha256(IDNumber) ] = now;
        return buTable[ sha256(IDNumber) ];
    }


    // checking if the timeout of user's session is expired
    function getPermission( string IDNumber, uint256 nowTime ) returns( bool ) {

        uint256 lastTime = permissionTable[ sha256(IDNumber) ];
        if( nowTime- lastTime > uint256( PermissionTimeOut ) ) {
            LogGetPermissionTimeExpired( sha256(IDNumber) );
            return false;
        } else {
            LogGetPermissionTimeValid( sha256(IDNumber) );
            return true;
        }

        return false;
    }

}

