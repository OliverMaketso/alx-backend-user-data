#!/usr/bin/env python3
"""
Route module for the API
"""
import os
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH_TYPE = getenv("AUTH_TYPE")


if AUTH_TYPE == "Auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request():
    """
    Execute before each request to filter requests based on authentication requirements.
    """
    print(f"Processing request path: {request.path}")

    # Check if auth is not None
    if auth is None:
        print("Auth is None, skipping authorization checks.")
        return

    # Check if path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        print(f"Request path {request.path} does not require authentication.")
        return

    # Check if the authorization header exists
    if auth.authorization_header(request) is None:
        print("Authorization header is missing, aborting with 401.")
        abort(401)

    # Check if current user exists
    if auth.current_user(request) is None:
        print("Current user is None, aborting with 403.")
        abort(403)



if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
