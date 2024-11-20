#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the salted hash.

    This function generates a salt using bcrypt.gensalt(), then hashes the
    password using bcrypt.hashpw() and the generated salt. The result is
    a salted hash of the password, which can be stored securely.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        bytes: The hashed password, including the salt, as a byte string.
    """
    # A randomly generated salt
    salt = bcrypt.gensalt()
    # Hash the password using the genrateed salt
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_passwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The email address of the user to register.
            password (str): The plain-text password of the user to register.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            # Checking if the user already exists in the database
            existing_user = self._db.find_user_by(email=email)
            # If a user exists, raise a valueError
            raise ValueError(f"User {existing_user.email} already exists")
        except NoResultFound:
            # If no existing user is found, preceed with registration
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
        except Exception as e:
            # Handling any other unexpected errors
            raise e
