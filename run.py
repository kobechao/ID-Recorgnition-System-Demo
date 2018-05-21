from Recognition_App import app

app.config.from_object( 'config' )
app.config.from_pyfile( 'config.py' )
app.secret_key = app.config['SECRET_KEY']

app.run( port=5000, debug=app.config['DEBUG'] )
