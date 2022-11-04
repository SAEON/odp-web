from flask import Flask

from odp.ui.dap.views import home, session


def init_app(app: Flask):
    app.register_blueprint(home.bp)
    app.register_blueprint(session.bp, url_prefix='/session')
