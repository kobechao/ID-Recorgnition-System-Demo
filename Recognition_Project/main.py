import os

from flask import ( Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, make_response )
from flask_script import Manager
from flask_login import ( LoginManager, UserMixin, login_user, current_user,  login_required, logout_user )
from models import User

app = Flask( __name__ )
# manager = Manager( app )

app.secret_key = 'FUCKYOU'
login_manager = LoginManager()
login_manager.init_app( app )

@login_manager.user_loader
def user_loader( user_id ):
	user = User()
	user.id = user_id
	return user


import contract
ID_Recognition_Contract = contract.ID_Recognition_Contract()

import pymysql
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
				sql = 'INSERT INTO personal_data ( userName,  birthday, personalID, marrige, family, education, occupation, password ) values ( \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\" );'
				# print( sql % ( form['name'], form['birthday'], form['personalID'], '', '', '', '', form['password'] ))							
				cursor.execute( sql % ( form['name'], form['birthday'], form['personalID'], '', '', '', '', form['password'] ))

				sql = 'INSERT INTO contract_data ( userName, contractAddress, contractABI, userToken ) values ( \"%s\", \"%s\", \"%s\", \"%s\" );'
				cursor.execute( sql % ( form['name'], ID_Recognition_Contract.address, ID_Recognition_Contract.contractABI, registerTx ))

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
		return '''
		     <form method='POST'>
		     <input type='text' name='personalID' id='personalID' placeholder='personalID'/>
		     <input type='password' name='password' id='password' placeholder='password'/>
		     <input type='submit' name='submit'/>
		     </form>
               '''

	elif request.method == 'POST':	
		form = request.form
		print( form )
		
		if form :			
			personalID = form.get( 'personalID', None )
			password = form.get( 'password', None )
			assert personalID is not None and password is not None

			print( personalID, password )

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


# Resuful URL: '/api/contract'
# ============================
@app.route('/api/contract', methods=['POST'])
@login_required
def getContractDataByName():

	if request.method == 'POST':
		form = request.form
		print( form )

		if form.get('name', None) :
			conn = connect_to_db()
			cursor = conn.cursor()

			sql = 'SELECT contractAddress, contractABI, userToken FROM contract_data WHERE userName=\'%s\';'
			cursor.execute( sql % form['name'] )

			userData = cursor.fetchone()
			# print( userData )

			cursor.close()
			conn.close()

			return jsonify({
					'userName': form['name'],
					'contractAddress': userData[0],
					'contractABI': userData[1],
					'userToken': userData[2],
					}), 201

		else:
			abort(404)

	else :
		abort(404)


# Resuful URL: '/api/userdata'
# @app.route('/api/userdata', methods=['POST'])
# def getUserDataByToken():

# 	if request.method == 'POST':
# 		form = request.form
# 		print( form )
# 		print( form.get('token', None) )

# 		if form.get('token', None) :
# 			conn = connect_to_db()
# 			cursor = conn.cursor()

# 			sql = "SELECT T1.userName, personalID, marrige, family, education, occupation FROM personal_data T1, contract_data T2 WHERE T1.userName = T2.userName and userToken = \'%s\' ;"
# 			print( sql )
# 			cursor.execute( sql % form['token'] )

# 			userData = cursor.fetchone()
# 			print( userData )

# 			cursor.close()
# 			conn.close()

# 			return jsonify({
# 					'userName': userData[0],
# 					'personalID': userData[1],
# 					'marrige': userData[2],
# 					'family': userData[3],
# 					'education': userData[4],
# 					'occupation': userData[5],
# 					}), 201

# 		else:
# 			abort(404)

# 	else :
# 		abort(404)


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