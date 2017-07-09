import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """docstring for Config"""
    SECRET_KEY = 'a secret_key string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """docstring for DevelopmentConfig"""

    DEBUG = True


class TestingConfig(Config):
    """docstring for TestConfig"""
    TESTING = True


class ProductionConfig(Config):
    """docstring for ProductionConfig"""
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
