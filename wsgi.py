import logging
import os

from werkzeug.middleware.proxy_fix import ProxyFix

from App import create_app

env = os.environ.get('FLASK_ENV', 'default')

application = create_app(env)
application.wsgi_app = ProxyFix(application.wsgi_app)
gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    application.run()
