from flask import Flask, Response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from routes.market import market_bp
import time
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Load configurations from the Config class
db = SQLAlchemy(app)
with app.app_context():
    Session = scoped_session(sessionmaker(bind=db.engine))
    db.create_all()
    db.session.commit()

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

from routes.otp import otp_bp
from routes.assets import assets_bp
from routes.subscriptions import subscription_bp
from routes.register import user_bp
from routes.session import session_bp
from routes.get_user_jnfo import get_user_info_bp
from routes.get_account_info import get_account_info_bp
from routes.transactions import transactions_bp
from routes.pin import pin_bp
from routes.trader import trader_bp
from models import TokenBlacklist


@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return Response("Access Denied", status=401, mimetype='text/plain')


@jwt.invalid_token_loader
def custom_invalid_token_response(callback):
    return Response("Access Denied", status=401, mimetype='text/plain')


@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return Response("Access Denied", status=401, mimetype='text/plain')


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return TokenBlacklist.query.filter_by(token=jti).first() is not None


@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return Response("Access Denied", status=401, mimetype='text/plain')


app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(session_bp, url_prefix='/api')
app.register_blueprint(get_user_info_bp, url_prefix='/api')
app.register_blueprint(get_account_info_bp, url_prefix='/api')
app.register_blueprint(otp_bp, url_prefix='/api')
app.register_blueprint(pin_bp, url_prefix='/api')
app.register_blueprint(transactions_bp, url_prefix='/api')
app.register_blueprint(assets_bp, url_prefix='/api')
app.register_blueprint(market_bp)
app.register_blueprint(subscription_bp, url_prefix='/api')
app.register_blueprint(trader_bp, url_prefix='/api')


def wait_for_mysql():
    while True:
        try:
            db.engine.execute('SELECT 1')
            print("MySQL is ready!")
            break
        except Exception:
            print("Waiting for MySQL...")
            time.sleep(3)


@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()


if __name__ == '__main__':
    app.run(debug=False)
