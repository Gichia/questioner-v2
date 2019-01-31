"""Configuration settings for the app"""
import os

class Config(object):
    """Main configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = "development"
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
    """Configurations for development"""
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    """Configurations for test"""
    FLASK_ENV = "testing"
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
}