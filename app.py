import os

from flask import make_response, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

from App import create_app

env = os.environ.get('FLASK_ENV', 'default')

app = create_app(env)
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
