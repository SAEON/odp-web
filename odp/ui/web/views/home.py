from flask import Blueprint, render_template

from odp.ui.base.forms import CatalogSearchForm

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template(
        'home.html',
        search_form=CatalogSearchForm(),
    )
