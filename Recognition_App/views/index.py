from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, abort
from Recognition_App.contract import getContractDBData
from Recognition_App.ApiExecuter import ApiExecuter
from flask_login import ( current_user, login_required, logout_user )
import requests, json


INDEX = Blueprint('index', __name__, template_folder='templates', static_folder='static', url_prefix='/index')

URLS_CONF = {
	'BANK': 'http://localhost:8001/api/BankData',
	'EDUCATION': 'http://localhost:8002/api/EducationData',
}

@INDEX.route('/', methods=['GET'])
def index() :

	if current_user.is_active :
		res = dict()
		contractData = getContractDBData( current_user.id )

		flash( 'Login as ' + session['userName'] )
		session['userid'] = current_user.id
		session['userToken'] = contractData.get( 'userToken', None )

		return render_template('index.html', res=res )
	
	else :
		return render_template('index.html')




@INDEX.route('/<url_institution>', methods=['GET', 'POST'] )
def institutionRegistration( url_institution ) :
	institution = url_institution.upper()

	if current_user.is_active and session['logged_in']:
		if request.method == 'POST':
			form = dict(request.form)

			if form.get( 'password', None )[0] == str(session['password']) :
				res = ApiExecuter( URLS_CONF[ institution ] + '/insertUserData', getContractDBData( current_user.id ), form ).getDBRespondData()
				flash( res[institution] )

			else :
				flash( 'Wrong Password!')

			return redirect( url_for('index.institutionRegistration', url_institution=url_institution) )


		else :
			# res = ApiExecuter( URLS_CONF[ institution ] + '/insertUserData', getContractDBData( current_user.id ), {'userName': 'kobe', 'birthday':'1996/09/23'} ).getDBRespondData()
			
			return render_template( '%s.html' % url_institution )

	else :
		return 'NOT LOGIN'


@INDEX.route('/profile', methods=['GET'])
def profile() :
	return render_template('profile.html')




@INDEX.route('/getAuthorizedDepartmentData', methods=['POST'])
def getAuthorizedDepartmentData() :
	form = dict( request.form )
	res = dict()
	print( form )

	if( form.get( 'userToken', None ) ) :

		contractData = getContractDBData( current_user.id )

		print( contractData.get( 'userToken', None ) )
		print( form[ 'userToken' ] )
		print( contractData.get( 'userToken', None ) == form[ 'userToken' ][0])

		if contractData.get( 'userToken', None ) == form[ 'userToken' ][0] :
			for department in URLS_CONF.keys():
				try :
					res[department] = ApiExecuter( URLS_CONF[department] + '/getUserData', contractData  ).getDBRespondData()
					print( department )

				except requests.exceptions.ConnectionError as err :
					print( 'Check Url Connection Of %s\n%s' % ( department, str( err ) ) )

			print( res )

			# return jsonify( res )
			return render_template('department_list.html', res=res )

		else :
			abort( 400, 'Wrong Token!' )

	else :
		abort( 400, 'No Token!' )



@INDEX.errorhandler(400) 
def errorHandler_400( err ) :
	response = jsonify( { 'message': err.description } )
	return response





