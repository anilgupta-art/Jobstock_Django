import requests

# Common query parameters for Zoho Recruit API list endpoints
ZOHO_COMMON_LIST_PARAMS = [
    'fields',        # Comma-separated list of fields to include in response
    'sort_by',       # Field to sort by
    'sort_order',    # asc or desc
    'page',          # Page number for pagination
    'per_page',      # Number of records per page
    'criteria',      # Filter criteria (Zoho query format)
    'search_text',   # Text search
    'include_child', # Include child records (boolean)
    'modified_since' # ISO date string for incremental fetch
]

def get_zoho_job_list(access_token, params=None):
    """
    Fetch the job list from Zoho Recruit using the provided access token.
    Args:
        access_token (str): Zoho OAuth access token.
        params (dict, optional): Query parameters for filtering, pagination, etc.
            Supported keys: fields, sort_by, sort_order, page, per_page, criteria, search_text, include_child, modified_since
    Returns:
        dict: Parsed JSON response from Zoho API (job list or error info).
    """
    url = 'https://recruit.zoho.com/recruit/v2/Jobs'
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except Exception:
        return {'error': 'Invalid response from Zoho.'}

def get_zoho_job_applicants(access_token, job_id, params=None):
    """
    Fetch the list of candidates who applied for a specific job in Zoho Recruit.
    Args:
        access_token (str): Zoho OAuth access token.
        job_id (str): The Zoho Job ID.
        params (dict, optional): Query parameters for filtering, pagination, etc.
            Supported keys: fields, sort_by, sort_order, page, per_page, criteria, search_text, include_child, modified_since
    Returns:
        dict: Parsed JSON response from Zoho API (applicant list or error info).
    """
    url = f'https://recruit.zoho.com/recruit/v2/Jobs/{job_id}/Candidates'
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except Exception:
        return {'error': 'Invalid response from Zoho.'}
