from flask import Blueprint, make_response, jsonify, request
from marshmallow import Schema, fields

from src.common.functions import check_request
from src.controllers.login import generate_temp_token

login_bp = Blueprint('user', __name__)

@login_bp.route('/authenticated', methods=['POST'])
def authenticated():
    class LoginSchema(Schema):
        user_id = fields.String(required=True, min=36, max=36)
        email = fields.String(required=True, max=255)
        unique_data = fields.String(required=True)

    data = check_request(LoginSchema(), request)
    return make_response(jsonify(generate_temp_token(data)), 200)


@login_bp.route('/login', methods=['POST'])
def login():
    class LoginSchema(Schema):
        email = fields.String(required=True, max=255)
        password = fields.String(required=True)

    data = check_request(LoginSchema(), request)
    return make_response(jsonify(generate_temp_token(data)), 200)