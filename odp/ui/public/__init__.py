from pathlib import Path

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader
from werkzeug.middleware.proxy_fix import ProxyFix

from odp.config import config
from odp.const import ODPScope
from odp.const.hydra import HydraScope
from odp.ui import base
from odp.ui.public import views


def create_app():
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=config.ODP.UI.PUBLIC.FLASK_KEY,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='Lax',
        CLIENT_ID=config.ODP.UI.PUBLIC.CLIENT_ID,
        CLIENT_SECRET=config.ODP.UI.PUBLIC.CLIENT_SECRET,
        CLIENT_SCOPE=[HydraScope.OPENID, HydraScope.OFFLINE_ACCESS, ODPScope.CATALOG_READ, ODPScope.TOKEN_READ],
        API_URL=config.ODP.UI.API_URL,
    )

    ui_dir = Path(__file__).parent.parent
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(ui_dir / 'public' / 'templates'),
        FileSystemLoader(base.TEMPLATE_DIR),
    ])
    app.static_folder = base.STATIC_DIR

    base.init_app(app)
    views.init_app(app)

    # trust the X-Forwarded-* headers set by the proxy server
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_prefix=1)

    return app
