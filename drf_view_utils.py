from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests

def call_drf_post_view(view_class, url, data):
    """
    Generic function to call a DRF APIView's post method with data and return the response.
    Args:
        view_class: The APIView class (not instance), e.g., ZohoRefreshTokenAPIView
        url: The URL string (not used for routing, but required by factory)
        data: The POST data as a dict
    Returns:
        DRF Response object
    """
    factory = APIRequestFactory()
    request = factory.post(url, data, format='json')
    view = view_class.as_view()
    response = view(request)
    return response

def rest_api_call(method, url, data=None, headers=None, params=None, timeout=30):
    """
    Generic function to make REST API calls using requests.
    Args:
        method: HTTP method as string (e.g., 'GET', 'POST', 'PUT', 'DELETE')
        url: Full URL to call
        data: Data to send (dict for JSON body or form data)
        headers: Optional headers dict
        params: Optional query parameters dict
        timeout: Timeout in seconds (default 30)
    Returns:
        requests.Response object
    """
    method = method.upper()
    if method == 'GET':
        return requests.get(url, headers=headers, params=params, timeout=timeout)
    elif method == 'POST':
        # Default to JSON if headers not specified
        if headers and 'application/x-www-form-urlencoded' in headers.get('Content-Type', ''):
            return requests.post(url, data=data, headers=headers, params=params, timeout=timeout)
        else:
            return requests.post(url, json=data, headers=headers, params=params, timeout=timeout)
    elif method == 'PUT':
        return requests.put(url, json=data, headers=headers, params=params, timeout=timeout)
    elif method == 'DELETE':
        return requests.delete(url, headers=headers, params=params, timeout=timeout)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

def get_django_auth_token(username):
    """
    Get or create a DRF token for a given username.
    Args:
        username: The username of the Django user.
    Returns:
        The token string, or None if user does not exist.
    """
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    token, created = Token.objects.get_or_create(user=user)
    return token.key

# Usage example (in any module):
# from drf_view_utils import get_django_auth_token
# token = get_django_auth_token('admin')
