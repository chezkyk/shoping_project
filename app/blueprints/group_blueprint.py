from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from app.database.postgres_connection import user_session_maker
from app.models.group_model import Group
from app.models.user_model import User
from app.models.groups_and_users import UserGroup

group_bp = Blueprint('group', __name__)


@group_bp.route('/create-group', methods=['POST'])
def create_group():
    try:
        # Get request data
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        group_name = data.get('group_name')
        address = data.get('address')

        # Check for required fields
        if not group_name or not address:
            return jsonify({"error": "Group name and address are required"}), 400

        # Create new group
        new_group = Group(
            group_name=group_name,
            address=address
        )
        with user_session_maker() as session:

        # Add to database
            session.add(new_group)
            session.commit()

            return jsonify({
                "message": "Group created successfully",
                "group": {
                    "id": new_group.id,
                    "group_name": new_group.group_name,
                    "address": new_group.address
                }
            }), 201

    except IntegrityError:
            session.rollback()
            return jsonify({"error": "A group with this name may already exist"}), 409

    except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500


@group_bp.route('/get-groups', methods=['GET'])
def get_groups():
    try:
        with user_session_maker() as session:
            # Retrieve all groups using session query
            groups = session.query(Group).all()

            # Prepare response
            groups_list = [{
                "id": group.id,
                "group_name": group.group_name,
                "address": group.address,
                "member_count": len(group.users)
            } for group in groups]

            return jsonify({
                "groups": groups_list,
                "total_groups": len(groups_list)
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@group_bp.route('/add-user-to-group', methods=['POST'])
def add_user_to_group():
    try:
        # Get request data
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        user_id = data.get('user_id')
        group_id = data.get('group_id')

        # Check for required fields
        if not user_id or not group_id:
            return jsonify({"error": "User ID and Group ID are required"}), 400

        with user_session_maker() as session:
            # Check if user exists
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Check if group exists
            group = session.query(Group).filter_by(id=group_id).first()
            if not group:
                return jsonify({"error": "Group not found"}), 404

            # Check if user is already in the group
            existing_membership = session.query(UserGroup).filter_by(
                user_id=user_id,
                group_id=group_id
            ).first()

            if existing_membership:
                return jsonify({"error": "User is already a member of this group"}), 400

            # Create new user-group association
            new_user_group = UserGroup(
                user_id=user_id,
                group_id=group_id
            )

            # Add to database
            session.add(new_user_group)
            session.commit()

            return jsonify({
                "message": "User added to group successfully",
                "user_id": user_id,
                "group_id": group_id
            }), 201

    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Could not add user to group"}), 409

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500