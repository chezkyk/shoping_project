from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from app.database.postgres_connection import user_session_maker
from app.models.group_model import Group


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
        # Retrieve all groups
        groups = Group.query(Group).all()

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