from flask import Blueprint

# from App.ext import Alipay, piPay

indexBlue = Blueprint('index_blue', __name__)


@indexBlue.route('/')
def index():
    return "index"
