from pathlib import Path

from flask import Flask

from odp.config import config
from odp.const import ODPCatalog, ODPScope
from odp.const.hydra import HydraScope
from odp.ui import base
from odp.ui.web import views


def create_app():
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.update(
        CATALOG_ID=ODPCatalog.SAEON,
        CATALOG_FACETS=[],
        UI_CLIENT_ID=config.ODP.WEB.UI_CLIENT_ID,
        UI_CLIENT_SECRET=config.ODP.WEB.UI_CLIENT_SECRET,
        UI_CLIENT_SCOPE=[
            HydraScope.OPENID,
            HydraScope.OFFLINE_ACCESS,
            ODPScope.CATALOG_READ,
            ODPScope.TOKEN_READ,
        ],
        CI_CLIENT_ID=config.ODP.WEB.CI_CLIENT_ID,
        CI_CLIENT_SECRET=config.ODP.WEB.CI_CLIENT_SECRET,
        CI_CLIENT_SCOPE=[
            ODPScope.CATALOG_READ,
        ],
        SECRET_KEY=config.ODP.WEB.FLASK_SECRET,
    )

    base.init_app(app, user_api=True, client_api=True, template_dir=Path(__file__).parent / 'templates')
    views.init_app(app)

    return app
