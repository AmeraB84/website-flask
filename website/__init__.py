from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


#Create database
db = SQLAlchemy()
DB_NAME = "database.db"

#create a flask app
def create_app():
    app =  Flask(__name__) # creare a app with name app
    app.config['SECRET_KEY'] = 'amera amera'

    #database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    #login manager 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # find logic of logging 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User,Note
    create_database(app)

    return app 

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
