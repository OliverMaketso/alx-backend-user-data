#!/usr/bin/env python3
"""
A session module that inherits from Auth
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


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
  

    def current_user(self, request=None):
        """
        Overload that returns a User instance based on a cookie value:
        Args:
            request: The incoming request object
        Returns:
            User instance or None if no valid session is found
        """
        # Get session ID from cookie
        session_id = self.session_cookie(request)

        # if no session ID is found, return None
        if session_id is None:
            return None
        
        # Get the user ID for the session ID
        user_id = self.user_id_for_session_id(session_id)

        # if no user ID is found, return None
        if user_id is None:
            return None
        
        # Fetch the user instance using the user ID
        user = User.get(user_id)

        return user
    

    def destroy_session(self, request=None):
        """
        Deletes the user session
        / logs out the user by removing the session ID.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
     
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False


if __name__ == "__main__":
    session_auth = SessionAuth()

    #  Checking if session_auth is an instance of Auth
    print(isinstance(session_auth, Auth))

    #  Checking if session_auth is an instance of SessionAuth
    print(isinstance(session_auth, SessionAuth))
