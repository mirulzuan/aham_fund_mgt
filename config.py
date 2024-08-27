import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fund_mgt_development.db'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fund_mgt_test.db'

class MigrationConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_DATABASE_URL') or 'mysql://aham:password@db/fund_mgt_development'
