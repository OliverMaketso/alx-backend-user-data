#!/usr/bin/env python3
"""
A session module that inherits from Auth
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    A Session-based authentication class
    """
    def __init__(self):
        super().__init__()  # Call the parent class's initializer
        self.user_id_by_session_id = {}  # Dict to store session - user mappings

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user_id
        Args:
            user_id (str): The ID of the user'
        Returns:
            str: The created Session ID, or None if user_id is invalid.
        """
        # Validating user_id
        if user_id is None or not isinstance(user_id, str):
            return None
 
        #Generate a unique Session ID
        session_id = str(uuid.uuid4())

        # store the mapping in the dictionary
        self.user_id_by_session_id[session_id] = user_id
   
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user id based on session id
        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The user ID associated with the session, or None if not found
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id, None)
if __name__ == "__main__":
    session_auth = SessionAuth()

    #  Checking if session_auth is an instance of Auth
    print(isinstance(session_auth, Auth))

    #  Checking if session_auth is an instance of SessionAuth
    print(isinstance(session_auth, SessionAuth))