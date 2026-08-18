from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user

from odp.config import config
from odp.lib.keycloak import JWTVerifier

bp = Blueprint('proxy', __name__)

jwt_verifier = JWTVerifier(f"{config.AUTH.URL}/protocol/openid-connect/certs")


@bp.route('/token')
def authenticate_access_token():
    """Implements token authentication."""
    try:
        auth_header = request.headers['Authorization']
        scheme, access_token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise ValueError
    except (KeyError, ValueError):
        abort(401)

    token = jwt_verifier.verify_token(access_token)
    if not token.active:
        abort(403)

    return dict(subject=token.sub)


@bp.route('/session')
def authenticate_session_cookie():
    """Implements session cookie authentication."""
    if not current_user.is_authenticated:
        abort(401)

    return dict(subject=current_user.id)


@bp.route('/unauthorized')
def unauthorized_user():
    """Implements redirect handler for unauthorized errors."""
    return redirect(url_for('auth.login', return_to=request.args.get('return_to')))
