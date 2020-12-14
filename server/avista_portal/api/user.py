from avista_portal.api import api_bp as bp
from avista_data import db
from avista_data.user import User
from flask import request, jsonify
from avista_portal.api import role_required
from avista_data.role import Role


@bp.route('/api/users', methods=['POST'])
@role_required(Role.ADMIN)
def create_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    response_object = {'status': 'success'}
    post_data = request.get_json()
    if post_data is None or post_data == {}:
        response_object['message'] = 'Missing data'
        response_object['status'] = 'failure'
        return jsonify(response_object), 400
    else:
        print("Post Data: " + str(post_data))
        user = User(post_data)
        db.session.add(user)
        db.session.commit()
        response_object['message'] = 'User added!'
        return jsonify(response_object), 200


@bp.route('/api/users', methods=['GET', 'POST'])
@role_required(Role.ADMIN)
def read_all_users():
    data = []
    for user in User.query.all():
        data.append(user.to_dict())
    response_object = data

    return jsonify(response_object)


@bp.route('/api/users/<int:user_id>', methods=['GET'])
@role_required(Role.USER)
def read_one_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    response_object = user.to_dict()

    return jsonify(response_object)


@bp.route('/api/users/<int:user_id>', methods=['PUT'])
@role_required(Role.USER)
def update_user(user_id):
    response_object = {'status': 'success'}

    post_data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    user.update(post_data)
    response_object['message'] = 'User updated!'

    return jsonify(response_object)


@bp.route('/api/users/<user_id>', methods=['DELETE'])
@role_required(Role.ADMIN)
def delete_user(user_id):
    response_object = {'status': 'success'}

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    response_object['message'] = 'User deleted!'

    return jsonify(response_object)
