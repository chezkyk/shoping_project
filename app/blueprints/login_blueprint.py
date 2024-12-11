from flask import Blueprint, request, jsonify

from app.database.postgres_connection import user_session_maker

from app.models.user_model import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])  # הגדרת השיטה כ-POST
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # פתיחת סשן למסד הנתונים
    with user_session_maker() as session:
        # חיפוש המשתמש לפי שם משתמש
        user = session.query(User).filter_by(username=username).first()

        if user and user.password == password:  # השוואה פשוטה של סיסמאות
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

