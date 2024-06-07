import pytest
from fastapi import HTTPException

from app.core.security.security import SecurityService


def test_access_token_creation_and_verification():

    to_encode = {'username': 'test', 'password': 'test'}

    # Create access token
    access_token = SecurityService.create_access_token(to_encode)
    assert access_token

    # Valid token
    data = SecurityService.verify_access_token(access_token)
    assert data
    assert data.get('username') == 'test'

    # Invalid token
    with pytest.raises(HTTPException):
        data = SecurityService.verify_access_token('invalid token')


def test_password_hashing_and_verification():

    password = 'test'
    hashed_password = SecurityService.get_password_hash(password)
    assert hashed_password
    assert SecurityService.verify_password(password, hashed_password)
    assert not SecurityService.verify_password('invalid', hashed_password)
