from flask import Blueprint, render_template, request, session, redirect, url_for
from Recognition_App.contract import getContractDBData
from Recognition_App.ApiExecuter import ApiExecuter
from flask_login import ( current_user, login_required, logout_user )


INDEX = Blueprint('index', __name__, template_folder='templates', static_folder='static')

URLS_CONF = {
	# 'BANK': 'http://localhost:8001/api/BankData',
	'EDUCATION': 'http://localhost:8002/api/EducationData',
}

@INDEX.route('/')
@INDEX.route('/index/')
def index() :
	if current_user.is_active :
		print( 'Login as ' + current_user.id )
		res = dict()
		for department in URLS_CONF.keys():
			print( department )
			res[department] = ApiExecuter( URLS_CONF[department], getContractDBData( current_user.id ) ).getRespondData()

		print( res )

	return render_template('index.html')


@INDEX.route('/logout/')
@login_required
def logout() :
	logout_user()
	session.pop( 'logged_in', None )

	return redirect( '/register/' )