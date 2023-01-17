from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from odp.config import config
from odp.ui.base import api

bp = Blueprint('data', __name__)


@bp.route('/')
def index():
    return render_template(
        'data.html',
        thredds_url=config.ODP.WEB.THREDDS_URL,
    )


@bp.route('/token')
def token():
    if current_user.is_authenticated:
        flash(api.token['access_token'], category='success')

    return redirect(url_for('.index'))
