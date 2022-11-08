from flask import Flask


def init_app(app: Flask):
    from . import catalog, home

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp, url_prefix='/catalog')
