from wtforms import StringField

from odp.ui.base.forms import BaseForm


class SearchForm(BaseForm):
    q = StringField()
