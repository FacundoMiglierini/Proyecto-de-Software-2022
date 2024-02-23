from os import environ
from datetime import timedelta


class Config(object):
    """Base conguration."""

    SECRET_KEY = "secret"
    DEBUG = False
    TESTING = False
    #JWT Token
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_SECRET_KEY = "secret_key"
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_ACCESS_CSRF_HEADER_NAME = "X-Xsrf-Token"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


# LAS SIGUIENTES HEREDAN DE LA PRIMERA:


class ProductionConfig(Config):
    """Production configuration."""
    
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )    
    # Session values
    SESSION_TYPE = "filesystem"

class DevelopmentConfig(Config):
    """Development configuration."""

    # Database values
    DEBUG = True
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_HOST = "localhost"
    DB_NAME = "grupo19"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    
    # Session values
    SESSION_TYPE = "filesystem"

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True


config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
}
