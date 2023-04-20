"""
The urls blueprint handles the user management for this application.
Specifically, this blueprint allows for users to add
url data from their database.
"""

# autopep8: off
from flask import Blueprint

urls_blueprint = Blueprint('urls', __name__, template_folder='templates')

from . import routes
# autopep8: on
