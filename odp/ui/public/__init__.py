from pathlib import Path

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader

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
        UI_CLIENT_ID=config.ODP.UI.PUBLIC.CLIENT_ID,
        UI_CLIENT_SECRET=config.ODP.UI.PUBLIC.CLIENT_SECRET,
        UI_CLIENT_SCOPE=[HydraScope.OPENID, HydraScope.OFFLINE_ACCESS, ODPScope.CATALOG_READ, ODPScope.TOKEN_READ],
    )

    ui_dir = Path(__file__).parent.parent
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(ui_dir / 'public' / 'templates'),
        FileSystemLoader(base.TEMPLATE_DIR),
    ])
    app.static_folder = base.STATIC_DIR

    base.init_app(app, user_api=True)
    views.init_app(app)

    return app
