import os
import platform
from datetime import timedelta

from redis import StrictRedis


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = "bbef6e33-ecb1-4f05-8651-8e781598876b"
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)


class DevelopConfig(Config):
    DEBUG = True
    redisHost = "127.0.0.1"
    redisPort = "6379"
    redisPassword = ""
    redisDateBaseIndex = "0"
    REDIS_URL = 'redis://:{0}@{1}:{2}/{3}'.format(redisPassword, redisHost, redisPort, redisDateBaseIndex)
    SESSION_REDIS = StrictRedis(host=redisHost, port=int(redisPort))


class ProductConfig(Config):
    redisHost = "127.0.0.1"
    redisPort = "6379"
    redisPassword = ""
    redisDateBaseIndex = "0"
    # REDIS_PASSWORD = "RmEdmC6cTfciNXW8"
    REDIS_URL = 'redis://:{0}@{1}:{2}/{3}'.format(redisPassword, redisHost, redisPort, redisDateBaseIndex)
    SESSION_REDIS = StrictRedis(host=redisHost, port=int(redisPort))


default = ProductConfig
if platform.system() == "Windows":
    default = DevelopConfig
if platform.system() == "Linux":
    default = ProductConfig

envs = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "default": default
}
