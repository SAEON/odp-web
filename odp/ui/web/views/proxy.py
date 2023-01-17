from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user

from odp.config import config
from odp.lib.hydra import HydraAdminAPI, OAuth2TokenIntrospection

bp = Blueprint('proxy', __name__)

hydra_admin_api = HydraAdminAPI(config.HYDRA.ADMIN.URL)


@bp.route('/token', methods=('POST',))
def authenticate_access_token():
    """Implements the Ory Oathkeeper bearer_token authenticator."""
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


@bp.route('/session', methods=('POST',))
def authenticate_session_cookie():
    """Implements the Ory Oathkeeper cookie_session authenticator."""
    if not current_user.is_authenticated:
        abort(401)

    return dict(subject=current_user.id)


@bp.route('/unauthorized')
def unauthorized_user():
    """Implements the Ory Oathkeeper redirect handler for unauthorized errors."""
    return redirect(url_for('hydra.login', return_to=request.args.get('return_to')))
