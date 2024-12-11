from flask import Flask, jsonify

from app.blueprints.group_blueprint import group_bp
from app.database.postgres_connection import user_engine
from app.init_db import initialize_db
from app.models import Base

from app.blueprints.login_blueprint import login_bp
from app.blueprints.sign_up_blueprint import sign_up_bp
Base.metadata.create_all(user_engine)
initialize_db()
app = Flask(__name__)
app.register_blueprint(login_bp)
app.register_blueprint(sign_up_bp)
app.register_blueprint(group_bp)

if __name__ == '__main__':
    app.run()