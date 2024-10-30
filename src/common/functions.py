from flask import Request
from marshmallow import ValidationError, Schema


def check_request(schema: Schema, request_data: Request) -> dict:
    """
    Checks request data against schema.
    :param schema: Schema
    :param request_data: Request
    :return: dict
    """
    try:
        data = schema.load(request_data.get_json())
        return data
    except ValidationError as err:
        raise KeyError(f'Fields errors: {str(err)}')
