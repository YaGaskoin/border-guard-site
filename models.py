from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_security import UserMixin, RoleMixin
from flask_security.forms import LoginForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired
import re


db = SQLAlchemy()
migrate = Migrate()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    slug = db.Column(db.String(140))
    created = db.Column(db.DateTime)
    author = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.created = datetime.now()
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title, self.created)


def slugify(title, date):
    pattern = r'\W'
    print(date)
    return re.sub(pattern, '_', (title + str(date)))


class Photos(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    link = db.Column(db.String(200), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=True)
    alert_id = db.Column(db.Integer(), db.ForeignKey('alert.id'), nullable=True)


roles_users = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))


class ExtendedLoginForm(LoginForm):
    email = StringField('Логин', [InputRequired()])
    password = PasswordField('Пароль', [InputRequired()])
    submit = SubmitField('Войти')
    remember = BooleanField('Запомнить меня')


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime)
    author = db.Column(db.String(100))
    slug = db.Column(db.String(200))

    def __init__(self, *args, **kwargs):
        super(Alert, self).__init__(*args, **kwargs)
        self.created = datetime.now()
        self.generate_slug()

    def generate_slug(self):
            self.slug = slugify('', self.created)
