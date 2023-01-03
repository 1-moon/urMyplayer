# a file to make python treat 
#   directories containing the file as packages 
from flask import Flask
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy
# Login manager instance let my app and flask-login work together 
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask_admin import Admin
from flask_moment import Moment

from flask_pagedown import PageDown
from config import config




# Constraint name should be defined using MetaData class.
# if we don't, database will occur an error "Constraint must have a name" 
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
#ORM(Object Relation Model)
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
moment = Moment()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name): 
    # allocate instance of Flask into app  
    app = Flask(__name__)  
    # to load this configuraiton into app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # flask administration set up
    admin = Admin(app, template_mode='bootstrap4')

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    moment.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    # # 템플릿 필터 직접 만들기
    # from .filter import format_datetime, format_date
    # app.jinja_env.filters['datetime'] = format_datetime
    # app.jinja_env.filters['date'] = format_date

    return app




