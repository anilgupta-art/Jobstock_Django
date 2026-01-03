def get_zoho_access_token_from_refresh(refresh_token, client_id, client_secret):
    token_url = 'https://accounts.zoho.com/oauth/v2/token'
    payload = {
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token'
    }
    resp = requests.post(token_url, data=payload)
    return resp.json()
def get_zoho_credentials_and_params(request):
    from global_settings_utils import get_setting_value
    from App.utils.json_read import dict_to_namespace
    setting = get_setting_value('ReetchUSA', 'ZohoCreditional')
    data = dict_to_namespace(setting.get('value') if setting else None)
    ResponseBody = dict_to_namespace(setting.get('ResponseBody'))
    grant_token = request.data.get('grant_token')
    client_id = data.client_id
    client_secret = data.client_secret
    redirect_uri = data.redirect_uri
    return {
        'setting': setting,
        'data': data,
        'ResponseBody': ResponseBody,
        'grant_token': grant_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }
def prepare_resume_folder(base_dir, subfolder='data/resume'):
    folder = os.path.join(base_dir, subfolder)
    os.makedirs(folder, exist_ok=True)
    return folder

def process_candidates_and_download_resumes(access_token, candidates, resume_folder):
    results = []
    for candidate in candidates:
        candidate_id = candidate.get('id')
        candidate_result = {'candidate_id': candidate_id, 'attachments': [], 'resume_saved': False}
        attachments = get_candidate_attachments(access_token, candidate_id)
        candidate_result['attachments'] = attachments
        if attachments:
            first_attachment = attachments[0]
            attachment_id = first_attachment.get('id')
            file_name = first_attachment.get('File_Name')
            if attachment_id:
                filepath = download_attachment_file(access_token, candidate_id, attachment_id, resume_folder, filename=file_name)
                if filepath:
                    candidate_result['resume_saved'] = True
                    candidate_result['resume_path'] = filepath
                else:
                    candidate_result['resume_saved'] = False
                    candidate_result['resume_error'] = 'Failed to download file.'
            else:
                candidate_result['resume_saved'] = False
                candidate_result['resume_error'] = 'No attachment_id found.'
        else:
            candidate_result['resume_saved'] = False
            candidate_result['resume_error'] = 'No attachments found.'
        results.append(candidate_result)
    return results
import requests
import os
import json

def get_zoho_access_token(grant_token, client_id, client_secret, redirect_uri):
    token_url = 'https://accounts.zoho.com/oauth/v2/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': grant_token,
    }
    resp = requests.post(token_url, data=token_data)
    return resp.json()

def get_zoho_candidates(access_token):
    url = 'https://recruit.zoho.com/recruit/v2/Candidates'
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
    resp = requests.get(url, headers=headers)
    return resp.json().get('data', [])

def get_candidate_attachments(access_token, candidate_id):
    url = f'https://recruit.zoho.com/recruit/v2/Candidates/{candidate_id}/Attachments'
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
    resp = requests.get(url, headers=headers)
    return resp.json().get('data', [])

def download_attachment_file(access_token, candidate_id, attachment_id, save_folder, filename=None):
    url = f'https://recruit.zoho.com/recruit/v2/Candidates/{candidate_id}/Attachments/{attachment_id}'
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
    resp = requests.get(url, headers=headers, stream=True)
    if resp.status_code == 200 and not resp.headers.get('Content-Type', '').startswith('application/json'):
        if not filename:
            filename = f'attachment_{attachment_id}'
        filepath = os.path.join(save_folder, filename)
        with open(filepath, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return filepath
    return None

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
