# a file configures application environment 

WTF_CSRF_ENABLED = True                # it determines if CSRF prevention should be enabled 



import os
#================== data base configuration ============#
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  # a key used to create cryptographically secure tokens 
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SECRET_KEY = 'LOVE-COMP2011'
    # MYCSW_ADMIN = os.environ.get('MYCSW_ADMIN')
    MYCSW_ADMIN = 'MYCSW_ADMIN'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

'''
    logging 
    to chase the events while program executes 
'''

# from logging.config import dictConfig
# dictConfig({
#     # safety control even if logging module upgrade 
#     'version': 1,
#     # format for printing log 
#     'formatters': {
#         'default': {
#             # defalut format - asctime: present time/ levelname: log level
#             # module" module name that calls log 
#             # message: output content 
#             'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#         }
#     },
#     # log printing method 
#     'handlers': {
#         # file handler 
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(basedir, 'logs/myproject.log'),
#             'maxBytes': 1024 * 1024 * 5,  # 5 MB
#             'backupCount': 5,
#             'formatter': 'default',
#         },
#     },
#     # the prime logger 
#     # log level : info
#     # handler for printing log as file format 
#     'root': {
#         'level': 'INFO',
#         'handlers': ['file']
#     }
# })