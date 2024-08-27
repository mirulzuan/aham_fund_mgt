import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fund_mgt_development.db'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fund_mgt_test.db'
