import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """docstring for Config"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a secret_key string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 30
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASK_COMMENTS_PER_PAGE = 30

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # 邮件标题及发件人名称，example.com 无用
    FLASKY_MAIL_SUBJECT_PREFIX = '[Blog-Instance]'
    FLASKY_MAIL_SENDER = 'Blog-Instance Admin <sender@example.com>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """docstring for DevelopmentConfig"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    """docstring for TestConfig"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """docstring for ProductionConfig"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
