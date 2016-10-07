# -*- coding: utf-8 -*-
__author__ = 'Pasturn'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jdkfja34234kjnsd'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CURSOR_MAIL_SUBJECT_PREFIX = '[Cursor]'
    CURSOR_MAIL_SENDER = 'Pasturn <pasturn@qq.com'
    CURSOR_ADMIN = os.environ.get('CURSOR_ADMIN') or 'admin@pasturn.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
                              or 'mysql+pymysql://root:67859253@localhost/blog?charset=utf8'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') \
                              or 'mysql+pymysql://root:67859253@localhost/blog/cms?charset=utf8'

class ProductionConfig(Config):
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
                              or 'mysql+pymysql://root:67859253@localhost/blog/cms?charset=utf8'

config = {
    'development': DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
