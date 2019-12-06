from logging.config import dictConfig

from flask import Flask, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

csp = {
    "default-src": [
        "'self'",
        'https://code.jquery.com/',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/',
        'https://stackpath.bootstrapcdn.com/bootstrap/',
        'https://www.youtube.com/',
        'https://bootstraplogos.com/wp-content/uploads/edd/2018/04/logo-1.png'
    ]
}

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

talisman = Talisman(content_security_policy=csp)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = b"0)\x08\xe3\xc9\xc8\x83\xb8\xf1\xda\xdb\xd7\xb3\x0eT\x17"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    talisman.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    #
    app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'testrbtest591@gmail.com',
    MAIL_PASSWORD = 'Testing1234',
    MAIL_DEFAULT_SENDER = 'testrbtest591@gmail.com',
   )

    mail.init_app(app)
    #

    from flask_app.main.routes import main
    from flask_app.users.routes import users
    from flask_app.posts.routes import posts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    with app.app_context():
        db.create_all()

    talisman.content_security_policy = csp
    talisman.content_security_policy_report_uri = "/csp_error_handling"

    return app
