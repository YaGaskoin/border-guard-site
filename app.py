from flask import Flask
from config import Conf
from models import db, migrate, User, Role, ExtendedLoginForm, Post
from flask_security import SQLAlchemyUserDatastore, Security
from flask_dropzone import Dropzone
from flask_msearch import Search


app = Flask(__name__)
app.config.from_object(Conf)

db.init_app(app)
app.db = db
migrate.init_app(app, db)
search = Search()
search.init_app(app)

dropzone = Dropzone(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm)




