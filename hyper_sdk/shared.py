"""Shared utility functions for both sync and async Session classes."""

from typing import Dict
from datetime import datetime, timedelta, timezone
import jwt


def generate_signature(key: str, secret: str) -> str:
    """
    Generates a JWT signature using the provided key and secret.

    Args:
        key (str): The key to include in the JWT claims
        secret (str): The secret used to sign the JWT

    Returns:
        str: The generated JWT token
    """
    claims = {
        "key": key,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=60)
    }
    token = jwt.encode(claims, secret, algorithm='HS256')
    return token.decode('utf-8') if type(token) == bytes else token


def build_headers(api_key: str, jwt_key: str = None, app_key: str = None, app_secret: str = None) -> Dict[str, str]:
    """
    Builds the headers dictionary including organization credentials if available.

    Args:
        api_key (str): The API key for authentication
        jwt_key (str, optional): The JWT key for signature generation
        app_key (str, optional): The application key
        app_secret (str, optional): The application secret

    Returns:
        Dict[str, str]: Headers dictionary with all required authentication headers

    Raises:
        ValueError: If api_key is not provided
    """
    if not api_key:
        raise ValueError("Missing API key")

    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    if jwt_key:
        signature = generate_signature(api_key, jwt_key)
        headers['X-Signature'] = signature

    if app_key and app_secret:
        app_signature = generate_signature(app_key, app_secret)
        headers['X-App-Signature'] = app_signature
        headers['X-App-Key'] = app_key

    return headers


def validate_response(response_data: dict, status_code: int) -> None:
    """
    Validates the API response and raises exceptions if there are errors.

    Args:
        response_data (dict): The parsed JSON response
        status_code (int): The HTTP status code

    Raises:
        Exception: If there's an error in the response or status code is not 200
    """
    if "error" in response_data and response_data["error"]:
        raise Exception(f"API returned with error: {response_data['error']}")

    if status_code != 200:
        raise Exception(f"API returned with status code: {status_code}")