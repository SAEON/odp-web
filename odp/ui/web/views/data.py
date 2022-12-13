from flask import Blueprint, abort, render_template
from flask_login import current_user

from odp.config import config

bp = Blueprint('data', __name__)


@bp.route('/')
def index():
    return render_template(
        'data.html',
        thredds_url=config.ODP.WEB.THREDDS_URL,
    )


@bp.route('/session')
def check_session():
    if not current_user.is_authenticated:
        abort(401)

    return {
        'subject': current_user.id,
        'extra': {},
    }
