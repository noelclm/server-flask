import logging
import time
import traceback

from flask import Flask, make_response, jsonify, g, request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from src.common.constants import ENV
from src.models import db
from src.routes.login import login_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(login_bp)


@app.route('/')
def test():
    return make_response(jsonify('OK'), 200)


@app.errorhandler(HTTPException)
def handle_exception(e):
    error_detail = f'{e.name} - {e.description}'
    app.logger.critical(f"Exception in {request.path}: \n{traceback.format_exc()} \nError details: {error_detail}")
    return make_response(jsonify(error_detail), e.code)


@app.errorhandler(KeyError)
@app.errorhandler(ValueError)
@app.errorhandler(TypeError)
@app.errorhandler(IndexError)
@app.errorhandler(AttributeError)
def handle_value_error(e):
    error_detail = str(e.orig) if hasattr(e, 'orig') else e.args[0]
    app.logger.error(f"Exception in {request.path}: \n{traceback.format_exc()} \nError details: {error_detail}")
    return make_response(jsonify(error_detail.splitlines()[0]), 400)


@app.errorhandler(PermissionError)
def handle_permission_error(e):
    error_detail = str(e.orig) if hasattr(e, 'orig') else e.args[0]
    app.logger.warning(f"Exception in {request.path}: {error_detail}")
    return make_response(jsonify(error_detail.splitlines()[0]), 401)


@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    error_detail = str(e.orig) if hasattr(e, 'orig') else e.args[0]
    app.logger.critical(f"Exception in {request.path}: \n{traceback.format_exc()} \nError details: {error_detail}")
    return make_response(jsonify(error_detail.splitlines()[0]), 400)


@app.errorhandler(Exception)
def handle_exception(e):
    error_detail = str(e.orig) if hasattr(e, 'orig') else e.args[0]
    app.logger.error(f"Exception in {request.path}: \n{traceback.format_exc()} \nError details: {error_detail}")
    return make_response(jsonify(error_detail.splitlines()[0]), 500)


@app.before_request
def log_request_info():
    g.debug = False
    g.start_time = time.time()
    g.client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    app.logger.info(f"REQUEST {request.method} {g.client_ip} {request.path} \"{request.user_agent}\"")
    app.logger.debug(f"Body: {request.get_data()}")


@app.after_request
def log_response_info(response):
    duration = time.time() - g.start_time
    app.logger.info(f"RESPONSE {g.client_ip} {request.path} {response.status} - Time {duration:.3f}")
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if ENV == 'LOCAL':
        app.logger.setLevel(logging.DEBUG)
        app.run(host="127.0.0.1", debug=True)
    else:
        app.logger.setLevel(logging.INFO)
