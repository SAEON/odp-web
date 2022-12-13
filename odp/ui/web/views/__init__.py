from flask import Flask


def init_app(app: Flask):
    from . import data, home
    from odp.ui.base.views import catalog

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp, url_prefix='/catalog')
    app.register_blueprint(data.bp, url_prefix='/data')
