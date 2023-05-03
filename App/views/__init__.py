from App.views.api import apiBlue
from App.views.index import indexBlue


# from App.views.index import index_blue

def init_view(app):
    app.register_blueprint(indexBlue)
    app.register_blueprint(apiBlue)
