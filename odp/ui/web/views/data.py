from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from odp.config import config
from odp.lib.hydra import HydraAdminAPI, OAuth2TokenIntrospection

bp = Blueprint('data', __name__)

hydra_admin_api = HydraAdminAPI(config.HYDRA.ADMIN.URL)


@bp.route('/')
def index():
    return render_template(
        'data.html',
        thredds_url=config.ODP.WEB.THREDDS_URL,
    )


@bp.route('/session', methods=('POST',))
def check_session():
    if not current_user.is_authenticated:
        abort(401)

    return dict(subject=current_user.id)


@bp.route('/token', methods=('POST',))
def check_token():
    try:
        auth_header = request.headers['Authorization']
        scheme, access_token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise ValueError
    except (KeyError, ValueError):
        abort(401)

    token: OAuth2TokenIntrospection = hydra_admin_api.introspect_token(access_token)
    if not token.active:
        abort(403)

    return dict(subject=token.sub)


@bp.route('/error')
def unauthorized_error():
    flash('Please log in to access that page.', category='warning')
    return redirect(url_for('.index'))
