#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        # Create a new User instance
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session
        self._session.add(new_user)

        # Commit the transaction to save the user to the database
        self._session.commit()

        # Return the newly created user
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.
        Returns:
            User: The first matching user.
        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            # Quering the users table and filter by the provided kwaags
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the specified parameters.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
         Updates a user's information based on the provided
         user_id and keyword arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments to update user attributes.

        Returns:
            None: This method does not return anything. It commits
            changes directly to the database.

        Raises:
            ValueError: If any invalid attribute is passed in kwargs.
            NoResultFound: If no user is found with the specified user_id.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound

        # Validating each key in kwargs corresponds to an existing User attr
        valid_cols = {column.name for column in User.__table__.columns}

        for key in kwargs:
            if key not in valid_cols:
                raise ValueError

        # Update
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit
        self._session.commit
