#!/usr/bin/env python3
""" Main 1
"""
import logging
from api.v1.auth.session_auth import SessionAuth

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sa = SessionAuth()

# log all attributes of the instance
logger.debug(f"Attributes of SessionAuth instance: {dir(sa)}")

# Log whether the attribute exists
if hasattr(sa, 'useer_id_by_session_id'):
    logger.info("Attribute 'user_by_session_id' exists.")
else:
    logger.error("Attribute 'user_id_by_session_id' does not exist.")




print("{}: {}".format(type(sa.user_id_by_session_id), sa.user_id_by_session_id))

user_id = None
session = sa.create_session(user_id)
print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

user_id = 89
session = sa.create_session(user_id)
print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

user_id = "abcde"
session = sa.create_session(user_id)
print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

user_id = "fghij"
session = sa.create_session(user_id)
print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

user_id = "abcde"
session = sa.create_session(user_id)
print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))
