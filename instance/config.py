"""Configuration settings for the app"""
import os

class Config(object):
    """Main configuration"""
    DEBUG = False
    TESTING = False
    ENV = "development"
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv("DATABASE_URL")

class Development(Config):
    """Configurations for development"""
    DEBUG = True
    TESTING = True

class Testing(Config):
    """Configurations for test"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")

class Staging(Config):
    """Configurations for staging"""
    DEBUG = False
    TESTING = False

class Production(Config):
    """Configurations for production"""
    DEBUG = False
    TESTING = False

config = {
    "development": Development,
    "testing": Testing,
    "staging": Staging,
    "production": Production
}