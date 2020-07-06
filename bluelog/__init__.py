from flask import Flask, render_template
import os
import click

from bluelog.blueprints import blog, admin, auth
from bluelog.blueprints.blog import blog_bp
from bluelog.settings import config
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.extensions import db, ckeditor, mail

#def make_app(config_name=None):



def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV','development')
    app = Flask('bluelog')
    app.config.from_object(config[config_name])
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_commands(app)
    register_errors(app)
    return app

def register_logging(app):
    pass
def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)
def register_template_context(app):
    pass
def register_commands(app):
    @app.cli.command()
    @click.option('--category', default = 10, help = 'Quantity of categories, default is 10.')
    @click.option('--post', default=50, help = 'Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generates the fake categories, posts, and comments."""
        from bluelog.fakes import fake_categories,fake_posts,fake_comments, fake_admim
        db.drop_all()
        db.create_all()
        click.echo('Generating the administrator...')
        fake_admim()
        click.echo('Generating %d categories...'% category)
        fake_categories()
        click.echo('Generating %d posts...' % post)
        fake_posts()
        click.echo('Generating %d comments...' % comment)
        fake_comments()
        click.echo('Done.')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request():
        return render_template('errors/400.html'), 400
#app.register_blueprint(auth_bp, url_prefix='/auth') #/auth/login
#app.register_blueprint(auth_bp,subdomain='auth') #auth.example.com/login
