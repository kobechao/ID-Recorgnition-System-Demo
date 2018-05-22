from flask import Flask
from .views.login import LOGIN
from .views.register import REGISTER
from .views.index import INDEX
from flask_login import LoginManager
from Recognition_App.models import User


app = Flask(__name__, instance_relative_config=True)
app.register_blueprint( LOGIN )
app.register_blueprint( REGISTER )
app.register_blueprint( INDEX, url_prefix='/index' )


login_manager = LoginManager()
login_manager.init_app( app )

@login_manager.user_loader
def user_loader( user_id ):
	user = User()
	user.id = user_id
	return user

from Recognition_App import views