import os
from datetime import timedelta


# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# # New MySQL Database Connection credentials
# db_user = 'emmanuel'
# db_pass = '01020304'
# db_name = 'flask'


class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='BAD_SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
    #                                     default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}")

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://emmanuel:01020304@localhost/flask"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=14)


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
