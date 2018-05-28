from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from Recognition_App.contract import getContractDBData
from Recognition_App.ApiExecuter import ApiExecuter
from flask_login import ( current_user, login_required, logout_user )
import requests


INDEX = Blueprint('index', __name__, template_folder='templates', static_folder='static', url_prefix='/index')

URLS_CONF = {
	'BANK': 'http://localhost:8001/api/BankData',
	'EDUCATION': 'http://localhost:8002/api/EducationData',
}

@INDEX.route('/', methods=['GET'])
def index() :

	if current_user.is_active :
		res = dict()
		for department in URLS_CONF.keys():
			try :
				res[department] = ApiExecuter( URLS_CONF[department] + '/getUserData', getContractDBData( current_user.id ) ).getDBRespondData()
				print( department )

			except requests.exceptions.ConnectionError as err :
				print( 'Check Url Connection Of %s\n%s' % ( department, str( err ) ) )

		print( res )
		flash( 'Login as ' + current_user.id )

		return render_template('index.html', res=res )
	
	else :
		return render_template('index.html' )




@INDEX.route('/<url_institution>', methods=['GET', 'POST'] )
def institutionRegistration( url_institution ) :
	institution = url_institution.upper()
	if current_user.is_active and session['logged_in']:
		if request.method == 'POST':
			form = dict(request.form)
			res = ApiExecuter( URLS_CONF[ institution ] + '/insertUserData', getContractDBData( current_user.id ), form ).getDBRespondData()
			return 'POST, %s, Login as %s' %( institution, current_user.id  )

		else :
			res = ApiExecuter( URLS_CONF[ institution ] + '/insertUserData', getContractDBData( current_user.id ), {'userName': 'kobe', 'birthday':'1996/09/23'} ).getDBRespondData()
			# print( res )
			return 'GET, %s, Login as %s' %( institution, current_user.id  )

	else :
		return 'NOT LOGIN'

