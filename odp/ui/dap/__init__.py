from pathlib import Path

from flask import Flask

from odp.config import config
from odp.const.hydra import HydraScope
from odp.ui import base
from odp.ui.dap import views


def create_app():
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=config.ODP.UI.DAP.FLASK_KEY,
        UI_CLIENT_ID=config.ODP.UI.DAP.CLIENT_ID,
        UI_CLIENT_SECRET=config.ODP.UI.DAP.CLIENT_SECRET,
        UI_CLIENT_SCOPE=[HydraScope.OPENID, HydraScope.OFFLINE_ACCESS],
    )

    base.init_app(app, user_api=True, template_dir=Path(__file__).parent / 'templates')
    views.init_app(app)

    return app
