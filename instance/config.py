"""Configuration settings for the app"""

class Config:
    """Main configuration"""
    DEBUG = False
    SECRET_KEY = 'try-to-finding-out'
    ENV = 'development'

class DevelopmentConfig:
    """Configurations for development"""
    pass

class TestConfig:
    """Configurations for test"""
    pass

class ProductionConfig:
    """Configurations for production""" 
    pass
