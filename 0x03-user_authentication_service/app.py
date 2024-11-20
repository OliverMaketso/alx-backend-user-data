#!/usr/bin/env python3
"""
A simple Flask app that returns a JSON response
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """"
    Route for the root ("/") URL that returns a JSON response.

    Returns:
        Jsonify: A JSON response with the message "Bienvenue".
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
