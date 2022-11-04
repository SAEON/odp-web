from flask import Flask

from odp.ui.public.views import catalog, home


def init_app(app: Flask):
    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp, url_prefix='/catalog')
