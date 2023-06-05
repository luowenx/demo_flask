import os
from flask import (
    Flask, render_template, session, redirect, jsonify
)
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'asasfsfsddssd'

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'book.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .views.auth import auth

    @app.route('/index')
    @auth
    def index():
        conection = db.get_db()
        query = 'SELECT * FROM book ORDER BY created DESC'
        cursor = conection.execute(query, ())
        books = cursor.fetchall()

        result_books = []
        for item in books:
            result_books.append({k: item[k] for k in item.keys()})
        cursor.close()
        return render_template('index.html', result_books=result_books)

    from .views import user
    from .views import sigin
    from .views import book

    app.register_blueprint(sigin.bp, url_prefix='/sigin')
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(book.bp, url_prefix='/book')

    db.init_app(app)

    return app
