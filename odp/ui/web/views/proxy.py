from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user

from odp.lib.auth import decode_and_verify_token

bp = Blueprint('proxy', __name__)


@bp.route('/token')
def authenticate_access_token():
    """Implements the Ory Oathkeeper bearer_token authenticator using Keycloak JWKS."""
    try:
        auth_header = request.headers['Authorization']
        scheme, access_token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise ValueError
    except (KeyError, ValueError):
        abort(401)

    try:
        claims = decode_and_verify_token(access_token)
    except Exception:
        abort(403)

    return dict(subject=claims.get('sub'))


@bp.route('/session')
def authenticate_session_cookie():
    """Implements the Ory Oathkeeper cookie_session authenticator."""
    if not current_user.is_authenticated:
        abort(401)

    return dict(subject=current_user.id)


@bp.route('/unauthorized')
def unauthorized_user():
    """Implements the Ory Oathkeeper redirect handler for unauthorized errors."""
    return redirect(url_for('hydra.login', return_to=request.args.get('return_to')))
