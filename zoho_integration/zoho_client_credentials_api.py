from django.conf import settings
import os
# ...existing code...

from rest_framework import permissions
from django.core.files.base import ContentFile


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os
import json
import requests
import base64

from App.settings.services import SettingService


from .models import ZohoTokenLog
from django.http import FileResponse

API_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'zoho_api_config.json')


# --- Separate APIView subclasses for each endpoint ---

class ZohoAuthCodeTokenAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get Zoho access token using authorization code grant",
        manual_parameters=[
            openapi.Parameter('grant_token', openapi.IN_QUERY, description="Zoho grant token (authorization code)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('client_id', openapi.IN_QUERY, description="Zoho client ID",value="1000.KPFB56O12AVTZGSWB0WBMS5X2XI0LC",  type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('client_secret', openapi.IN_QUERY, description="Zoho client secret",value="9c39beb5ee700593f3a445505e235989c05720152a", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('redirect_uri', openapi.IN_QUERY, description="Redirect URI",value="http://localhost:8000", type=openapi.TYPE_STRING, required=True),
             openapi.Parameter('Scope', openapi.IN_QUERY, description="Scope",value="ZohoRecruit.modules.ALL,ZohoRecruit.jobs.ALL", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: openapi.Response('Token response', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                'expires_in': openapi.Schema(type=openapi.TYPE_INTEGER),
                'token_type': openapi.Schema(type=openapi.TYPE_STRING),
                'error': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))}
    )
    def get(self, request):
        from global_settings_utils import get_setting_value
        from App.utils.json_read import dict_to_namespace
        # Example usage: replace 'your_client' and 'your_key' with actual values or variables
        setting = get_setting_value('ReetchUSA', 'ZohoCreditional')
        # setting will be a dict like {'key': ..., 'value': ...} or None
        data=dict_to_namespace(setting.get('value') if setting else None)
        grant_token = request.GET.get('grant_token')
        client_id =data.client_id # request.GET.get('client_id')
        client_secret = data.client_secret # request.GET.get('client_secret')
        redirect_uri = data.redirect_uri # request.GET.get('redirect_uri')
        if not all([grant_token, client_id, client_secret, redirect_uri]):
            return Response({'error': 'grant_token, client_id, client_secret, and redirect_uri are required.'}, status=status.HTTP_400_BAD_REQUEST)
        token_url = 'https://accounts.zoho.com/oauth/v2/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': grant_token,
        }
        try:
            response = requests.post(token_url, data=data)
        except Exception as e:
            return Response({'error': f'Failed to connect to Zoho: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
        try:
            tokens = response.json()
            SettingService.update_setting(setting_key='ZohoCreditional', data=tokens)
        except Exception:
            return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
        if not response.ok or 'error' in tokens:
            return Response({'error': tokens.get('error', 'Failed to obtain token'), 'details': tokens}, status=response.status_code)
        # If refresh_token is present, exchange for access token
        # if tokens.get('refresh_token'):
        #     payload = {
        #         'refresh_token': tokens.get('refresh_token'),
        #         'client_id': client_id,
        #         'client_secret': client_secret,
        #         'grant_type': 'refresh_token'
        #     }
        #     try:
        #         resp2 = requests.post(token_url, data=payload)
        #         tokens2 = resp2.json()
        #     except Exception:
        #         return Response({'error': 'Invalid response from Zoho (refresh token).'}, status=status.HTTP_502_BAD_GATEWAY)
        #     if not resp2.ok or 'error' in tokens2:
        #         return Response({'error': tokens2.get('error', 'Failed to obtain access token from refresh token'), 'details': tokens2}, status=resp2.status_code)
        #     return Response(tokens2, status=status.HTTP_200_OK)
        # return Response(tokens, status=status.HTTP_200_OK)

class ZohoRefreshTokenAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Generate Zoho access token from refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Zoho OAuth2 refresh token'),
                'client_id': openapi.Schema(type=openapi.TYPE_STRING, description='Zoho client ID'),
                'client_secret': openapi.Schema(type=openapi.TYPE_STRING, description='Zoho client secret'),
            },
            required=['refresh_token', 'client_id', 'client_secret']
        ),
        responses={200: openapi.Response('Token response', openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def post(self, request):
        from global_settings_utils import get_setting_value
        from App.utils.json_read import dict_to_namespace   
        setting = get_setting_value('ReetchUSA', 'ZohoCreditional')
        data=dict_to_namespace(setting.get('value') if setting else None)
        ResponseBody=dict_to_namespace(setting.get('ResponseBody') )#if setting else None)
        refresh_token = ResponseBody.refresh_token        
        #refresh_token = request.data.get('refresh_token')
        client_id =data.client_id # request.GET.get('client_id')
        client_secret = data.client_secret # request.GET.get('client_secret')
        if not all([refresh_token, client_id, client_secret]):
            return Response({'error': 'refresh_token, client_id, and client_secret are required.'}, status=status.HTTP_400_BAD_REQUEST)
        token_url = 'https://accounts.zoho.com/oauth/v2/token'
        payload = {
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token'
        }
        response = requests.post(token_url, data=payload)
        try:
            token_resp = response.json()
        except Exception:
            return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
        if 'access_token' in token_resp:           
            SettingService.update_setting(setting_key='ZohoCreditional', data=token_resp,ResponseBody=ResponseBody)
            return Response(token_resp, status=status.HTTP_200_OK)
        return Response(token_resp, status=status.HTTP_400_BAD_REQUEST)

class ZohoCandidatesAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get Zoho candidates using access token",
        manual_parameters=[
            openapi.Parameter('access_token', openapi.IN_QUERY, description="Zoho access token", type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: openapi.Response('Candidate List', openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        access_token = request.GET.get('access_token')
        if not access_token:
            return Response({'error': 'access_token query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        candidates_url = 'https://recruit.zoho.com/recruit/v2/Candidates'
        headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
        response = requests.get(candidates_url, headers=headers)
        try:
            data = response.json()
        except Exception:
            return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
        if response.status_code == 200:
            return Response(data)
        return Response(data, status=response.status_code)

class ZohoResumeDownloadAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Download resume for a specific candidate",
        manual_parameters=[
            openapi.Parameter('candidate_id', openapi.IN_QUERY, description="Zoho candidate ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('access_token', openapi.IN_QUERY, description="Zoho access_token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('refresh_token', openapi.IN_QUERY, description="Zoho candidate ID", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response('Resume file'),
            400: openapi.Response('Error response', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            ))
        }
    )
    def get(self, request):
        candidate_id = request.GET.get('candidate_id')
        access_token = request.GET.get('access_token')
        refresh_token = request.GET.get('refresh_token')
        if not candidate_id:
            return Response({'error': 'candidate_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with open(API_CONFIG_PATH, 'r') as f:
                creds = json.load(f)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #access_token = creds.get('access_token')
        if not access_token and refresh_token:
            token_url = 'https://accounts.zoho.com/oauth/v2/token'
            payload = {
                'refresh_token': creds['refresh_token'],
                'client_id': creds['client_id'],
                'client_secret': creds['client_secret'],
                'grant_type': 'refresh_token'
            }
            resp2 = requests.post(token_url, data=payload)
            try:
                token_resp = resp2.json()
            except Exception:
                return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
            access_token = token_resp.get('access_token')
            if not access_token:
                return Response({'error': 'Could not obtain access token from refresh token', 'zoho_response': token_resp}, status=status.HTTP_400_BAD_REQUEST)
        if not access_token:
            return Response({'error': 'No access token or refresh token found in config.'}, status=status.HTTP_400_BAD_REQUEST)
        resume_url = f'https://recruit.zoho.com/recruit/v2/Candidates/{candidate_id}/downloadresume'
        headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
        response = requests.get(resume_url, headers=headers)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            content_disp = response.headers.get('Content-Disposition', f'attachment; filename="resume_{candidate_id}.pdf"')
            resp = Response(response.content, content_type=content_type)
            resp['Content-Disposition'] = content_disp
            return resp
        try:
            data = response.json()
        except Exception:
            data = {'error': 'Invalid response from Zoho.'}
        return Response(data, status=response.status_code)
    

class ZohoCandidateAttachmentListAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of attachments for a candidate from Zoho using access token and candidate_id.",
        manual_parameters=[
            openapi.Parameter('access_token', openapi.IN_QUERY, description="Zoho access token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('candidate_id', openapi.IN_QUERY, description="Zoho candidate ID", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response('Attachment list', openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response('Error response', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            ))
        }
    )
    def get(self, request):
        access_token = request.GET.get('access_token')
        candidate_id = request.GET.get('candidate_id')
        if not all([access_token, candidate_id]):
            return Response({'error': 'access_token and candidate_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        url = f'https://recruit.zoho.com/recruit/v2/Candidates/{candidate_id}/Attachments'
        headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
        response = requests.get(url, headers=headers)
        try:
            data = response.json()
        except Exception:
            data = {'error': 'Invalid response from Zoho.'}
        if response.status_code == 200:
            return Response(data)
        return Response(data, status=response.status_code)

class ZohoCandidateAttachmentAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get a candidate's attachment from Zoho using access token and candidate_id.",
        manual_parameters=[
            openapi.Parameter('access_token', openapi.IN_QUERY, description="Zoho access token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('candidate_id', openapi.IN_QUERY, description="Zoho candidate ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('attachment_id', openapi.IN_QUERY, description="Zoho attachment ID", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response('Attachment file'),
            400: openapi.Response('Error response', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
            ))
        }
    )
    def get(self, request):
        access_token = request.GET.get('access_token')
        candidate_id = request.GET.get('candidate_id')
        attachment_id = request.GET.get('attachment_id')
        if not all([access_token, candidate_id, attachment_id]):
            return Response({'error': 'access_token, candidate_id, and attachment_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        url = f'https://recruit.zoho.com/recruit/v2/Candidates/{candidate_id}/Attachments/{attachment_id}'
        headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}
        response = requests.get(url, headers=headers, stream=True)
        content_type = response.headers.get('Content-Type', '')
        # If the response is a file (not JSON), return as file using FileResponse
        if response.status_code == 200 and not content_type.startswith('application/json'):
            content_disp = response.headers.get('Content-Disposition', f'attachment; filename="attachment_{attachment_id}"')
            file_response = FileResponse(response.raw, content_type=content_type or 'application/octet-stream')
            file_response['Content-Disposition'] = content_disp
            return file_response
        # Otherwise, try to parse as JSON (error case)
        try:
            data = response.json()
        except Exception:
            data = {'error': 'Invalid response from Zoho.'}
        return Response(data, status=response.status_code)

class ZohoBulkResumeDownloadAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        operation_description="Get Zoho access token, candidate list, attachments, and download resumes to /data/resume/.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'grant_token': openapi.Schema(type=openapi.TYPE_STRING, description='Zoho grant token (authorization code)'),
                'client_id': openapi.Schema(type=openapi.TYPE_STRING,value="1000.KPFB56O12AVTZGSWB0WBMS5X2XI0LC", description='Zoho client ID'),
                'client_secret': openapi.Schema(type=openapi.TYPE_STRING,value="9c39beb5ee700593f3a445505e235989c05720152a", description='Zoho client secret'),
                'redirect_uri': openapi.Schema(type=openapi.TYPE_STRING,value="http://localhost:8000", description='Redirect URI'),
                'Scope': openapi.Schema(type=openapi.TYPE_STRING,value="ZohoRecruit.modules.ALL", description='ZohoRecruit.modules.ALL'),
            },
#        {
#   "grant_token": "1000.92b4b3020ffe34ac6c644ce3343db7fc.ca46a8d15c3b522428338d0126a92c0c",
#   "client_id": "1000.KPFB56O12AVTZGSWB0WBMS5X2XI0LC",
#   "client_secret": "9c39beb5ee700593f3a445505e235989c05720152a",
#   "redirect_uri": "http://localhost:8000",
#   "Scope": "ZohoRecruit.modules.ALL"
# }
            required=['grant_token', 'client_id', 'client_secret', 'redirect_uri']
        ),
        responses={200: openapi.Response('Bulk download result', openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def post(self, request):
        from global_settings_utils import get_setting_value
        from App.utils.json_read import dict_to_namespace
        from .zoho_api_utils import (
            get_zoho_access_token, get_zoho_candidates,
            prepare_resume_folder, process_candidates_and_download_resumes,get_zoho_job_list
        )
        from .zoho_api_utils import get_zoho_credentials_and_params
        params = get_zoho_credentials_and_params(request)
        setting = params['setting']
        data = params['data']
        ResponseBody = params['ResponseBody']
        grant_token = params['grant_token']
        client_id = params['client_id']
        client_secret = params['client_secret']
        redirect_uri = params['redirect_uri']

        # Step 1: Get access token
        tokens = get_zoho_access_token(grant_token, client_id, client_secret, redirect_uri)
        access_token = tokens.get('access_token')
        # If no access_token, try refresh_token logic
        if not access_token:
            refresh_token = ResponseBody.refresh_token
            if refresh_token:
                from .zoho_api_utils import get_zoho_access_token_from_refresh
                tokens = get_zoho_access_token_from_refresh(refresh_token, client_id, client_secret)
                access_token = tokens.get('access_token')
                if not access_token:
                    return Response({'error': 'Failed to obtain access token from refresh token', 'details': tokens}, status=status.HTTP_400_BAD_REQUEST)
                SettingService.update_setting(setting_key='ZohoCreditional', data=tokens, ResponseBody=ResponseBody)
            else:
                return Response({'error': 'Failed to obtain access token', 'details': tokens}, status=status.HTTP_400_BAD_REQUEST)
        else:
            SettingService.update_setting(setting_key='ZohoCreditional', data=tokens, ResponseBody=ResponseBody)

        joblist=get_zoho_job_list(access_token)
        # Step 2: Get candidate list
        candidates = get_zoho_candidates(access_token)
        if not candidates:
            return Response({'error': 'No candidates found'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare resume folder
        resume_folder = prepare_resume_folder(settings.BASE_DIR)
        # Step 3: Process candidates and download resumes
        results = process_candidates_and_download_resumes(access_token, candidates, resume_folder)
        return Response({'results': results, 'resume_folder': resume_folder})
# Utility: Bulk resume download without DRF request (for scheduler/CLI)
def zoho_bulk_resume_download_no_request():
    """
    Run Zoho bulk resume download logic without a DRF request object.
    Loads credentials and params from .env/settings.
    Returns a dict with results and resume folder path.
    """
    from global_settings_utils import get_setting_value
    from App.utils.json_read import dict_to_namespace
    from .zoho_api_utils import (
        get_zoho_access_token, get_zoho_candidates,
        prepare_resume_folder, process_candidates_and_download_resumes, get_zoho_job_list
    )
    from App.settings.services import SettingService
    from django.conf import settings

    # Load Zoho credentials from settings/.env
    setting = get_setting_value('ReetchUSA', 'ZohoCreditional')
    data = dict_to_namespace(setting.get('value') if setting else None)
    ResponseBody = dict_to_namespace(setting.get('ResponseBody'))
    grant_token = getattr(data, 'grant_token', None)
    client_id = getattr(data, 'client_id', None)
    client_secret = getattr(data, 'client_secret', None)
    redirect_uri = getattr(data, 'redirect_uri', None)

    # Step 1: Get access token
    tokens = get_zoho_access_token(grant_token, client_id, client_secret, redirect_uri)
    access_token = tokens.get('access_token')
    # If no access_token, try refresh_token logic
    if not access_token:
        refresh_token = getattr(ResponseBody, 'refresh_token', None)
        if refresh_token:
            from .zoho_api_utils import get_zoho_access_token_from_refresh
            tokens = get_zoho_access_token_from_refresh(refresh_token, client_id, client_secret)
            access_token = tokens.get('access_token')
            if not access_token:
                return {'error': 'Failed to obtain access token from refresh token', 'details': tokens}
            SettingService.update_setting(setting_key='ZohoCreditional', data=tokens, ResponseBody=ResponseBody)
        else:
            return {'error': 'Failed to obtain access token', 'details': tokens}
    else:
        SettingService.update_setting(setting_key='ZohoCreditional', data=tokens, ResponseBody=ResponseBody)

    joblist = get_zoho_job_list(access_token)
    # Step 2: Get candidate list
    candidates = get_zoho_candidates(access_token)
    if not candidates:
        return {'error': 'No candidates found'}

    # Prepare resume folder
    resume_folder = prepare_resume_folder(settings.BASE_DIR)
    # Step 3: Process candidates and download resumes
    results = process_candidates_and_download_resumes(access_token, candidates, resume_folder)
    return {'results': results, 'resume_folder': resume_folder}
