#!/usr/bin/env python3
"""
An SQLAlchemy model for the 'users' table
This module defines a 'User' class mapped to the users table,
which represents the user data.
"""
import sqlalchemy
from sqlalchemy.orm.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Base class for defining ORM models
Base = declarative_base()


class User(Base):
    """
    User class representing a record in the 'users' database table.
    Attributes:
        id (int): Unique identifier for the user (Primary Key).
        email (str): User's email address (Non-Nullable).
        hashed_password (str): User's hashed password (Non-Nullable).
        session_id (Optional[str]): ID of the current session (Nullable).
        reset_token (Optional[str]): Token used for password resets (Nullable).
    """
    __tablename__: str = 'users'  # Table name in the database

    # Columns definitions with type annotations
    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String(250), nullable=False)
    hashed_password: Column = Column(String(250), nullable=False)
    session_id: Column = Column(String(250), nullable=True)
    reset_token: Column = Column(String(250), nullable=True)
