#!/usr/bin/env python3
"""
A simple Flask app that returns a JSON response
"""
from flask import Flask, jsonify, redirect, request, abort, make_response
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """"
    Route for the root ("/") URL that returns a JSON response.

    Returns:
        Jsonify: A JSON response with the message "Bienvenue".
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    Route for the /users that registers users

    Returns:
        JSON
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Login endpint
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logging out endpint
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        response = make_response(redirect('/'))
        response.delete_cookie('session_id')
        return response
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Profile endpoint that returns the user's email if the session ID is valid.
    
    The request is expected to contain a 'session_id' cookie. The function uses this 
    session ID to find the user. If the session is valid and the user exists, it returns 
    the user's email in the JSON response with a 200 HTTP status. If the session ID is invalid 
    or the user does not exist, it responds with a 403 Forbidden status.
    
    Returns:
        tuple: A tuple containing a JSON response with the user's email and a status code.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Reset password endpoint"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Update password endpoint"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
