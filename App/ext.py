from concurrent.futures import ThreadPoolExecutor

import pymongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_redis import FlaskRedis
from loguru import logger
from shortid import ShortId

from App.sdk.DouBanClient import DouBanClient
from App.utiles.ip2Region import Ip2Region
from App.utiles.mailServer import MailServer

limiter = Limiter(key_func=get_remote_address)
redis_client = FlaskRedis()
executor = ThreadPoolExecutor(32)
ShortIdGen = ShortId()
mailServer = MailServer()
ip2region = Ip2Region("ip2region.db")
LogLevel = "DEBUG"
logger.add('logs/baseExt.log',
           level=LogLevel,
           format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {file} - {line} - {message}',
           rotation="10 MB")
baseLogger = logger.bind(name="baseExt")
mongoDbIp = "10.0.0.40"
mongoDbPort = 27017
mongoDbUserName = None
mongoDbPass = '$K3zF%vwvpz6pD'
mongoDbMaxPoolSize = 100
if mongoDbUserName is not None:
    client = pymongo.MongoClient(host=mongoDbIp, port=mongoDbPort, username=mongoDbUserName,
                                 password=mongoDbPass,
                                 maxPoolSize=mongoDbMaxPoolSize)
else:
    client = pymongo.MongoClient(host=mongoDbIp, port=mongoDbPort, maxPoolSize=mongoDbMaxPoolSize)
mongodb = client.movieDb
douBanClient = DouBanClient()
MovieCollection = mongodb.movie
personCollection = mongodb.person


def init_ext(app):
    limiter.init_app(app)
    redis_client.init_app(app)
    mailServer.init_app(app)
