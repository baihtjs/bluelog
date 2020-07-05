from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()