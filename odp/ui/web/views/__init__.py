from flask import Flask


def init_app(app: Flask):
    from . import data, home, proxy
    from odp.ui.base.views import catalog, package, vocabulary

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp, url_prefix='/catalog')
    app.register_blueprint(package.bp, url_prefix='/package')
    app.register_blueprint(vocabulary.bp, url_prefix='/vocabulary')
    app.register_blueprint(data.bp, url_prefix='/data')
    app.register_blueprint(proxy.bp, url_prefix='/proxy')
