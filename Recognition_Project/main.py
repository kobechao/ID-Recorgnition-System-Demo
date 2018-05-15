import os

from flask import ( Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, make_response )
from flask_script import Manager
app = Flask(__name__)
manager = Manager(app)

import contract
ID_Recognition_Contract = contract.ID_Recognition_Contract()

import pymysql
def connect_to_db() :
	conn = pymysql.connect( host='127.0.0.1', user='root', passwd='tina1633', db='DBO_BLOCKCHAIN')
	return conn

# Route: '', '/index'
@app.route('/')
@app.route('/index/')
def index() :
	return render_template('index.html')

# Route: '/register'
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

			print( registerTx )

			conn = connect_to_db()
			cursor = conn.cursor()

			try :
				sql = 'INSERT INTO personal_data ( userName,  birthday, personalID, passportID, marrige, family, education, occupation, password ) values ( \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\" );'
				# print( sql % ( form['name'], form['birthday'], form['personalID'], form['passportID'], form['marrige'], form['family'], form['education'], form['occupation'] ))							
				#cursor.execute( sql % ( form['name'], form['birthday'], form['personalID'], form['passportID'], form['marrige'], form['family'], form['education'], form['occupation'], form['password'] ))
				cursor.execute( sql % ( form['name'], form['birthday'], form['personalID'], '', '', '', '', '', form['password'] ))
				sql = 'INSERT INTO contract_data ( userName, contractAddress, contractABI, userToken ) values ( \"%s\", \"%s\", \"%s\", \"%s\" );'
				# print( sql % ( form['name'], ID_Recognition_Contract.address, ID_Recognition_Contract.contractABI, registerTx ) )
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
		error = 'FUCK'


# Route: '/signin'
@app.route('/signin/')
def signin() :
	return 'signin'


# Route: '/logout'
@app.route('/logout/')
def logout() :
	return redirect( '/register' )


# Resuful URL: '/contract'
@app.route('/contract', methods=['POST'])
def getContractDataByName():

	if request.method == 'POST':
		form = request.form
		print( form )

		if form.get('name', None) :
			conn = connect_to_db()
			cursor = conn.cursor()

			sql = 'SELECT contractAddress, contractABI, userToken FROM contract_data WHERE name=\'%s\';'
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


# Error Handler
@app.errorhandler(404)
def not_found( error ) :
	return make_response( jsonify({
			'error': 'Not Found'
		}), 404)


if __name__ == '__main__':
	# app.run(port=8000, debug=True)
	manager.run()