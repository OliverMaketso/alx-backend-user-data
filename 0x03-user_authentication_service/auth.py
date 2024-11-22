#!/usr/bin/env python3
"""
Authentication module
"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB
from user import User
from typing import Optional
import uuid


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


def _generate_uuid() -> str:
    """
    Generates a new UUID AND RETURNS ITS STRINg representation.

    Retturns:
        str: A string representation of a newUUID.
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's email and password.

        Args:
            email (str): The user's email address.
            password (str): The plaintext password to check.

        Returns:
             bool: True if the user exists and the password is
             correct, False otherwise>
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # comparing the plintext pass with the stored hashed pass
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password):
                return True

        except Exception as e:
            print(f"Error during login validation: {e}")

        return False

    def create_session(self, email: str) -> str:
        """
        Create a session ID for the user corresponding to the provided email.

        Args:
            email (str): The user's email address

        Returns:
            Optional[str]: The session ID if the user exists, None otherwise.
        """
        try:
            # finding the user by email
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves the user associated with a given session ID from
        the database.

        Args:
            session_id (str): The session ID to search for.

        Returns:
            User: The user associated with the session ID if found.
            None: If no user is found or if the session_id is None.

        Raises:
            NoResultFound: If the database query doesn't find any
            matching user.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroys session
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset password token for valid user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password after resetting"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            hashed_pwd = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_pwd, reset_token=None)
