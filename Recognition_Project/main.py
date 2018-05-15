import os
import pymysql

from flask import ( Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, make_response )
from flask_script import Manager
from flask_login import ( LoginManager, UserMixin, login_user, current_user,  login_required, logout_user )

from models import User
from ApiExecuter import ApiExecuter
from contract import ID_Recognition_Contract, getContractDBData

app = Flask( __name__ )
# manager = Manager( app )

app.secret_key = 'FUCKYOU'
login_manager = LoginManager()
login_manager.init_app( app )

ID_Recognition_Contract = ID_Recognition_Contract()

URLS_CONF = {
	'BANK': 'http://localhost:8001/api/BankData',
	# 'EDUCATION': 'http://localhost:8002/api/EducationData',
}


@login_manager.user_loader
def user_loader( user_id ):
	user = User()
	user.id = user_id
	return user


def connect_to_db() :
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	return conn



# Route: '', '/index'
# ===================
@app.route('/')
@app.route('/index/')
def index() :
	if current_user.is_active :
		print( 'Login as ' + current_user.id )
		res = dict()
		for department in URLS_CONF.keys():
			res[department] = ApiExecuter( URLS_CONF[department], getContractDBData( current_user.id ) ).getRespondData()

		print( res )

	return render_template('index.html')



# Route: '/register'
# ==================
@app.route('/register/', methods=['GET', 'POST']) 
def register() :

	error = None

	if request.method == 'GET':
		return render_template( 'register.html' )

	elif request.method == 'POST':
		form = request.form
		print( 'post:', form)

		if ID_Recognition_Contract.getUserRegisterTable( form.get( 'name', None ) ) :
			flash( 'Has Data' )
			return redirect( '/register')

		else :
			registerTx = ID_Recognition_Contract.setUserRegisterTable( form.get( 'name', None ) ).hex()
			assert ID_Recognition_Contract.getUserRegisterTable( form.get( 'name', None ) ) == True
			assert registerTx != None

			conn = connect_to_db()
			cursor = conn.cursor()

			try :
				sql = 'INSERT INTO personal_data ( userName,  birthday, personalID, marrige, family, education, occupation, password ) values ( \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");'
				print( sql % ( form['name'], form['birthday'], form['personalID'], '', '', '', '', form['password'] ))							
				cursor.execute( sql % ( form['name'], form['birthday'], form['personalID'], '', '', '', '', form['password'] ))

				sql = 'INSERT INTO contract_data ( personalID, contractAddress, contractABI, userToken ) values ( \"%s\", \"%s\", \"%s\", \"%s\" );'
				cursor.execute( sql % ( form['personalID'], ID_Recognition_Contract.address, ID_Recognition_Contract.contractABI, registerTx ))

				conn.commit()

			except Exception as e :
				flash( str(e) )
				print( type(e), e )

			finally:
				cursor.close()
				conn.close()

			return redirect('/register/')

	else :
		pass



# Route: '/login'
# ================
@app.route( '/login/', methods = ['GET', 'POST'] )
def login() :
	if request.method == 'GET' :
		# return '''
		#      <form method='POST'>
		#      <input type='text' name='personalID' id='personalID' placeholder='personalID'/>
		#      <input type='password' name='password' id='password' placeholder='password'/>
		#      <input type='submit' name='submit'/>
		#      </form>
  #              '''
  		return render_template( 'login.html' )
  		

	elif request.method == 'POST':	
		form = request.form
		# print( form )
		
		if form :			
			personalID = form.get( 'personalID', None )
			password = form.get( 'password', None )
			assert personalID is not None and password is not None

			conn = connect_to_db()
			cursor = conn.cursor()

			try:
				sql = 'SELECT personalID, password FROM personal_data where personalID=\'%s\';' 
				print( sql )
				cursor.execute( sql % personalID )
				userLoginData = cursor.fetchone()

				if userLoginData is None:
					print( 'No Such User' )
					return redirect( url_for('login') )

				if personalID == userLoginData[0] and password == userLoginData[1] :
					print( 'login success!!!' )

					user = User()
					user.id = personalID
					login_user( user )

					return redirect( url_for('index') )

				else :
					
					print( 'Wrong Password' )
					return redirect( url_for('login') )


			except Exception as e:
				return str(e)
			
			finally:
				cursor.close()
				conn.close()



# Route: '/logout'
# =================
@app.route('/logout/')
@login_required
def logout() :
	logout_user()

	return redirect( url_for('register') )



# Error Handler
# ==============
@app.errorhandler(404)
def not_found( error ) :
	return make_response( jsonify({
			'error': 'Not Found'
		}), 404)



# test
# =====
@app.route('/tmp', methods=['GET'] )
@login_required
def test() :
	if current_user.is_active:
		return 'Login as ' + current_user.id
	else :
		return 'YO'



if __name__ == '__main__':
	app.run( port=5000, debug=True )
	# manager.run()