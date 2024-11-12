#!/usr/bin/env python3
"""Authentication module."""
from flask import request
from typing import List, TypeVar
import fnmatch


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
        :oaram request: The Flask request object
        """
        return None
 