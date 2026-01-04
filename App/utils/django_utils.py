from rest_framework.test import APIRequestFactory

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
