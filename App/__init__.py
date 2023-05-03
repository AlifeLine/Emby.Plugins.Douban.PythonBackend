import datetime
import decimal
import json

from bson import ObjectId
from flask import Flask

from App.ext import init_ext
from App.settings import envs
from App.views import init_view


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(envs.get(env))
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.config['PROPAGATE_EXCEPTIONS'] = True
    # 初始化api
    init_ext(app)
    # 初始化路由
    init_view(app)
    app.json_encoder = DateEncoder
    return app
