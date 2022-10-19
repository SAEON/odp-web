from wtforms import StringField

from odp.ui.forms import BaseForm


class SearchForm(BaseForm):
    q = StringField()
