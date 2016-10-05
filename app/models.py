__author__ = 'Pasturn'

import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from . import db
from urllib.parse import urlparse, urlunparse

unicode = str


# 权限角色模型
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('Users', backref = 'role', lazy = 'dynamic')

    # 在数据库中创建角色
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMIT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMIT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Roles.query.filter_by(name=r).first()
            if role is None:
                role = Roles(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01
    COMMIT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


# 用户模型
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    # registered_date = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default = datetime.datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default = datetime.datetime.utcnow)
    posts = db.relationship('Posts', backref = 'author', lazy = 'dynamic')



    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['CURSOR_ADMIN']:
                self.role = Roles.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Roles.query.filter_by(default=True).first()


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成一个令牌，有效期为一个小时
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # dumps生成一个加密签名
        return s.dumps({'confirm': self.user_id})

    # 检验令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # 解码令牌，序列化对象
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.user_id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

    # 在请求和赋予角色这两种权限之间进行位操作
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.add(self)

    def is_authenticated(self):
        return True
    # 修复id属性不一致
    def get_id(self):
        try:
            return unicode(self.user_id)  # python 2
        except NameError:
            return str(self.user_id)  # python 3

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default= datetime.datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))



@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.user_id == int(user_id)).first()
