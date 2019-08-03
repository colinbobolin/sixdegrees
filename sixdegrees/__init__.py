import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sixdegrees.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        # # a simple page that says hello
        # @app.route('/hello')
        # def hello():
        #     return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import game
    app.register_blueprint(game.bp)

    return app




# app = Flask(__name__)
#
# import sixdegrees.views
#
# from . import db
#     db.init_app(app)