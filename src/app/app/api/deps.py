from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from motor.core import AgnosticDatabase

from app import crud, models, schemas
from app.core.config import settings
from app.database.session import MongoDatabase

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/oauth")


def get_db() -> Generator:
    try:
        db = MongoDatabase()
        yield db
    finally:
        pass


async def get_user_id():
    """
    A simple function that returns a fixed user ID for testing purposes.
    In a real application, this would parse a token or session.
    """
    # Return a constant test user ID
    return "test-user-id-123"

async def is_admin():
    """
    A simple function that always returns True for testing purposes.
    In a real application, this would check the user's permissions.
    """
    # Always return True to grant admin access during testing
    return True