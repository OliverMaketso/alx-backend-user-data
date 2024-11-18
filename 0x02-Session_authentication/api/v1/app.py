#!/usr/bin/env python3
"""
Route module for the API

This module initializes a Flask application, sets up authentication, error handling,
and route filtering based on authentication requirements.
"""
import os
from typing import Optional, Any
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth import auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth: Optional[Auth] = None  #Authentication handler instance
AUTH_TYPE: Optional[str]= os.getenv("AUTH_TYPE")  # Determines the type of authentication to use


# Set up the appropruate authentication handler based on AUTH_TYPE
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


# print(f"AUTH_TYPE: {AUTH_TYPE}")  # Debugging print to check AUTH_TYPE
# print(f"Auth instance: {type(auth)}")  # Debugging

excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/', '/api/v1/auth_session/login/']


@app.errorhandler(404)
def not_found(error) -> str:
    """ Handler for 404 Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Handler for 401 unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """Handler for 403 Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> Optional[Any]:
    """
    Execute before each request to filter requests based
    on authentication requirements.
    - If 'auth' is None, skips authentication.
    - checks if the requested path is in 'excluded_paths'.
      If yes, slips authentication.
    - verifies the presence of Authorization header. 
    If missing, aborts with a 401
    - verifies the current user. If None, aborts witha 403 error
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


    if auth.session_cookie(request) is None:
        abort(401)

    # Check if current user exists
    current_user = auth.current_user(request)
    if auth.current_user(request) is None:
        print("Current user is None, aborting with 403.")
        abort(403)

    # Assign the current user to request.current_user
    request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
