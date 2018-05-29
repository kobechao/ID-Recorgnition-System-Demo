from flask import ( Blueprint, render_template, request, redirect, session, url_for )
from .MYSQL import connect_to_db
from flask_login import ( login_user, current_user, logout_user, login_required )
from Recognition_App.models import User

LOGIN = Blueprint('login', __name__, template_folder='templates', static_folder='static')

@LOGIN.route( '/login/', methods = ['GET', 'POST'] )
@LOGIN.route( '/signin/', methods = ['GET', 'POST'] )
def login() :
	if request.method == 'GET' :
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
				# print( sql )
				cursor.execute( sql % personalID )
				userLoginData = cursor.fetchone()

				if userLoginData is None:
					print( 'No Such User' )
					return redirect( url_for('login.login') )

				if personalID == userLoginData[0] and password == userLoginData[1] :
					user = User()
					user.id = personalID
					login_user( user )

					session['logged_in'] = True
					session['password'] = password

					return redirect( url_for('index.index') )

				else :
					
					print( 'Wrong Password' )
					return redirect( url_for('login.login') )


			except Exception as e:
				return str(e)
			
			finally:
				cursor.close()
				conn.close()

@LOGIN.route('/logout/')
@login_required
def logout() :
	print('logout')
	logout_user()
	session.pop( 'logged_in', None )
	session.pop( 'userid', None )
	session.pop( 'password', None )

	return redirect( url_for('register.register') )


