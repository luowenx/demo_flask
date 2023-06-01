from flask import Blueprint

bp = Blueprint('user', __name__)


@bp.route('/info')
def user_info():
    return 'user is info'