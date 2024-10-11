from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.testing.pickleable import User

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_db():
    db.create_all()
    print("Database created")


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '<KEY>'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))


    from .views import views
    from .admin import admin
    from .auth import auth
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        create_db()

    return app





