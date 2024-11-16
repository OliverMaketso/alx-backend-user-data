#!/usr/bin/env python3
"""Authentication module."""
from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """Basic authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a specific path requires authentication.
        param path: path to be checked
        param excluded_paths: List of paths that do not require authentication
        Returns:
            False - path
            excluded_paths
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a requests.
        :param request: The flask request object
        :return: The Authorization header value, or None if not present.
        """
        if request is None:
            return None
    
        if 'Authorization' not in request.headers:
            return None
 
        return request.headers.get('Authorization')


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from a request.
        :param request: The Flask request object
        """
        return None
    
    
    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
        `   request (Request): The request object containing the cookies.

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None
        
        # Get the session cookie name from the environment variable SESSION_NAME
        session_cookie_name = os.getenv('SESSION_NAME', '_my_session_id')

        # use .get() to access the cookie value safely from request's cookies
        return request.cookies.get(session_cookie_name, None)
        

 