def connect_to_db() :
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	return conn