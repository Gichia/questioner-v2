""" Create custom error messages """
from flask import jsonify, make_response
from app.api import ver2

@ver2.errorhandler(405)
def bad_request(error):
    """Error to catch not allowed method"""
    return make_response(jsonify({"error": "Method not allowed!", "status": 405}), 405)

@ver2.errorhandler(500)
def internal_server_error(error):
    """Error to catch internal server error"""
    return make_response(jsonify({"error": "Internal error!", "status": 500}), 500)

@ver2.errorhandler(404)
def not_found(error):
    """Error to catch page not found"""
    return make_response(jsonify({"error": "Resource not found!", "status": 404}), 404)
