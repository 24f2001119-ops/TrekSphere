from flask import Blueprint

staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff",
    template_folder="../templates/staff"
)

from . import routes