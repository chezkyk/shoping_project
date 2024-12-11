from flask import Blueprint,request, jsonify

from app.database.postgres_connection import user_session_maker
from app.models.user_model import User

sign_up_bp = Blueprint('sign_up', __name__)

@sign_up_bp.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    address = data.get('address')

    if not username or not password or not address:
        return jsonify({'error': 'Username, password, and address are required'}), 400

    # פתיחת סשן למסד הנתונים
    with user_session_maker() as session:
        # בדיקה אם המשתמש כבר קיים
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'User with this username already exists'}), 409

        # הוספת משתמש חדש
        new_user = User(username=username, password=password, address=address)
        session.add(new_user)
        session.commit()

        return jsonify({'message': 'User successfully signed up'}), 201