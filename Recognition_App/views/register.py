from flask import Blueprint, render_template, request
from .MYSQL import connect_to_db
from Recognition_App.contract import ID_Recognition_Contract, getContractDBData


REGISTER = Blueprint('register', __name__, template_folder='templates', static_folder='static')


@REGISTER.route('/register/', methods=['GET', 'POST']) 
def register() :

	error = None

	if request.method == 'GET':
		return render_template( 'register.html' )

	elif request.method == 'POST':
		form = request.form
		print( 'post:', form)

		if ID_Recognition_Contract.getUserRegisterTable( userID=form['name'] ) :
			flash( 'Has Data' )
			return redirect( '/register')

		else :
			registerTx = ID_Recognition_Contract.setUserRegisterTable( userID=form['name'] ).hex()
			assert ID_Recognition_Contract.getUserRegisterTable( userID=form['name'] ) == True
			assert registerTx != None

			conn = connect_to_db()
			cursor = conn.cursor()

			try :
				sql = 'INSERT INTO personal_data ( userName,  birthday, personalID, marrige, family, education, occupation, password ) values ( \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");'
				# print( sql % ( form['name'], form['birthday'], form['personalID'], '', '', '', '', form['password'] ))							
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