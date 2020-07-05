from flask import Blueprint

admin_bp = Blueprint('admin',__name__,template_folder='templates')
@admin_bp.route('/index')
def index():
    return 'Hello admin index'