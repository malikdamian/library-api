from flask import Response, jsonify

from library_app import db
from library_app.errors import errors_pb


class ErrorResponse:

    def __init__(self, message: str, http_status: int):
        self.payload = {
            'success': False,
            'message': message
        }
        self.http_status = http_status

    def to_response(self) -> Response:
        response = jsonify(self.payload)
        response.status_code = self.http_status
        return response


@errors_pb.app_errorhandler(400)
def handle_400(error):
    messages = error.data.get('messages', {}).get('json', {})
    return ErrorResponse(messages, 400).to_response()


@errors_pb.app_errorhandler(401)
def handle_401(error):
    return ErrorResponse(error.description, 401).to_response()


@errors_pb.app_errorhandler(404)
def handle_404(error):
    return ErrorResponse(error.description, 404).to_response()


@errors_pb.app_errorhandler(409)
def handle_409(error):
    return ErrorResponse(error.description, 409).to_response()


@errors_pb.app_errorhandler(415)
def handle_415(error):
    return ErrorResponse(error.description, 415).to_response()


@errors_pb.app_errorhandler(500)
def handle_500(error):
    db.session.rollback()
    return ErrorResponse(error.description, 500).to_response()
