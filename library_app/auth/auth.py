from flask import jsonify, abort
from webargs.flaskparser import use_args

from library_app import db
from library_app.auth import auth_bp
from library_app.models import user_schema, User, UserSchema, user_password_update_schema
from library_app.utils import validate_json_content_type, token_required


@auth_bp.post('/register')
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description=f'User with username {args["username"]} already exists')

    if User.query.filter(User.email == args['email']).first():
        abort(409, description=f'User with email {args["email"]} already exists')

    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token
    }), 201


@auth_bp.post('/login')
@validate_json_content_type
@use_args(UserSchema(only=['username', 'password']), error_status_code=400)
def login(args: dict):
    user = User.query.filter(User.username == args['username']).first()
    if not user:
        abort(401, description='Invalid credentials')

    if not user.is_password_valid(args['password']):
        abort(401, description='Invalid credentials')

    token = user.generate_jwt()
    return jsonify({
        'success': True,
        'token': token,
    })


@auth_bp.get('/me')
@token_required
def get_current_user(user_id: int):
    user = User.query.get_or_404(user_id,
                                 description=f'User with id {user_id} not found')
    data = user_schema.dump(user)
    return jsonify(
        {'success': True,
         'data': data}
    )


@auth_bp.put('/update/password')
@token_required
@validate_json_content_type
@use_args(user_password_update_schema, error_status_code=400)
def update_password(user_id: int, args: dict):
    user = User.query.get_or_404(user_id,
                                 description=f'User with id: {user_id} not found')

    if not user.is_password_valid(args['current_password']):
        abort(401, description='Invalid password')

    user.password = user.generate_hashed_password(args['new_password'])

    db.session.commit()

    data = user_schema.dump(user)
    return jsonify(
        {'success': True,
         'data': data}
    )


@auth_bp.put('/update/data')
@token_required
@validate_json_content_type
@use_args(UserSchema(only=['username', 'email']), error_status_code=400)
def update_user_data(user_id: int, args: dict):
    user = User.query.get_or_404(user_id,
                                 description=f'User with id: {user_id} not found')

    if User.query.filter(
            User.username == args['username'], user.username != args['username']
    ).first():
        abort(409, description=f'User with username {args["username"]} already exists')
    if User.query.filter(
            User.email == args['email'], user.email != args['email']
    ).first():
        abort(409, description=f'User with email {args["email"]} already exists')

    user.username = args['username']
    user.email = args['email']

    db.session.commit()

    data = user_schema.dump(user)
    return jsonify(
        {'success': True,
         'data': data}
    )
