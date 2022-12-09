from pathlib import Path

from flask import Flask

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
        UI_CLIENT_ID=config.ODP.UI.PUBLIC.CLIENT_ID,
        UI_CLIENT_SECRET=config.ODP.UI.PUBLIC.CLIENT_SECRET,
        UI_CLIENT_SCOPE=[HydraScope.OPENID, HydraScope.OFFLINE_ACCESS, ODPScope.CATALOG_READ, ODPScope.TOKEN_READ],
    )

    base.init_app(app, user_api=True, template_dir=Path(__file__).parent / 'templates')
    views.init_app(app)

    return app
