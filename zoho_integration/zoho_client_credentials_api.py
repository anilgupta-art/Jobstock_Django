class ZohoResumeDownloadAPI(APIView):
    """
    API endpoint to download a candidate's resume from Zoho Recruit.
    """
    @swagger_auto_schema(
        operation_description="Download candidate resume from Zoho Recruit",
        manual_parameters=[
            openapi.Parameter('candidate_id', openapi.IN_QUERY, description="Zoho Candidate ID", type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: openapi.Response('Resume File', openapi.Schema(type=openapi.TYPE_STRING, format='binary'))}
    )
    def get(self, request):
        candidate_id = request.GET.get('candidate_id')
        if not candidate_id:
            return Response({'error': 'candidate_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Load Zoho API config
        try:
            with open(API_CONFIG_PATH, 'r') as f:
                creds = json.load(f)
        except Exception as e:
            return Response({'error': f'Failed to load API config: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get access token (refresh if needed)
        access_token = creds.get('access_token')
        if not access_token and creds.get('refresh_token'):
            token_resp = ZohoClientCredentialsTokenAPI().generate_access_token_from_refresh_token(
                creds['refresh_token'], creds['client_id'], creds['client_secret']
            )
            access_token = token_resp.get('access_token')
            if not access_token:
                return Response({'error': 'Could not obtain access token from refresh token', 'zoho_response': token_resp}, status=status.HTTP_400_BAD_REQUEST)

        if not access_token:
            return Response({'error': 'No access token or refresh token found in config.'}, status=status.HTTP_400_BAD_REQUEST)

        # Zoho Recruit API endpoint for resume download
        resume_url = f'https://recruit.zoho.com/recruit/v2/Candidates/{candidate_id}/downloadresume'
        headers = {
            'Authorization': f'Zoho-oauthtoken {access_token}'
        }
        response = requests.get(resume_url, headers=headers)
        if response.status_code == 200:
            # Return file as attachment
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            content_disp = response.headers.get('Content-Disposition', f'attachment; filename="resume_{candidate_id}.pdf"')
            return Response(response.content, content_type=content_type, headers={'Content-Disposition': content_disp})
        try:
            data = response.json()
        except Exception:
            data = {'error': 'Invalid response from Zoho.'}
        return Response(data, status=response.status_code)
# class ZohoCandidateListAPI(APIView):
#     """
#     API endpoint to fetch candidate list from Zoho Recruit.
#     """
#     @swagger_auto_schema(
#         operation_description="Get candidate list from Zoho Recruit",
#         responses={200: openapi.Response('Candidate List', openapi.Schema(type=openapi.TYPE_OBJECT))}
#     )
#     def get(self, request):
#         # Load Zoho API config
#         try:
#             with open(API_CONFIG_PATH, 'r') as f:
#                 creds = json.load(f)
#         except Exception as e:
#             return Response({'error': f'Failed to load API config: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Get access token (assume it's stored or use refresh_token flow)
#         access_token = creds.get('access_token')
#         if not access_token and creds.get('refresh_token'):
#             # Try to get new access token from refresh token
#             token_resp = generate_access_token_from_refresh_token(
#                 creds['refresh_token'], creds['client_id'], creds['client_secret']
#             )
#             access_token = token_resp.get('access_token')
#             if not access_token:
#                 return Response({'error': 'Could not obtain access token from refresh token', 'zoho_response': token_resp}, status=status.HTTP_400_BAD_REQUEST)

#         if not access_token:
#             return Response({'error': 'No access token or refresh token found in config.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Zoho Recruit API endpoint for candidates
#         candidates_url = 'https://recruit.zoho.com/recruit/v2/Candidates'
#         headers = {
#             'Authorization': f'Zoho-oauthtoken {access_token}'
#         }
#         response = requests.get(candidates_url, headers=headers)
#         try:
#             data = response.json()
#         except Exception:
#             return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
#         if response.status_code == 200:
#             return Response(data)
#         return Response(data, status=response.status_code)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import os
import json
import requests
from .models import ZohoTokenLog

API_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'zoho_api_config.json')

class ZohoClientCredentialsTokenAPI(APIView):
    @swagger_auto_schema(
        operation_description="Get Zoho OAuth token using client_credentials grant (reads from zoho_api_config.json)",
        responses={200: openapi.Response('Token response', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                'expires_in': openapi.Schema(type=openapi.TYPE_INTEGER),
                'token_type': openapi.Schema(type=openapi.TYPE_STRING),
                'error': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))}
    )
    def get2(self, request):
        def log_token_response(data):
            ZohoTokenLog.objects.create(
                token_type=data.get('token_type', ''),
                access_token=data.get('access_token', ''),
                expires_in=data.get('expires_in', 0),
                error=data.get('error', None)
            )

        try:
            with open(API_CONFIG_PATH, 'r') as f:
                creds = json.load(f)
        except Exception as e:
            return Response({'error': f'Failed to load API config: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        url = 'https://accounts.zoho.com/oauth/v2/token'
        payload = {
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'grant_type': creds['grant_type'],
            'scope': creds['scope'],
            'soid': creds['soid']
        }
        response = requests.post(url, data=payload)
        try:
            data = response.json()
        except Exception:
            return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
        log_token_response(data)
        if response.status_code == 200 and 'access_token' in data:
            return Response(data)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

    import requests

    def get(self, request):

        # Fill these with your Zoho Self Client credentials and grant token
        grant_token = '1000.c253905f720dde7d21ba0dadf1b3c75b.bbd14c69e0575c813966eb9caaefc33e'
        client_id = '1000.KPFB56O12AVTZGSWB0WBMS5X2XI0LC'
        client_secret = '9c39beb5ee700593f3a445505e235989c05720152a'
        redirect_uri = 'http://localhost:8000'  # Must match the one in Zoho Self Client

        token_url = 'https://accounts.zoho.com/oauth/v2/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': grant_token,
        }
        #1000.25b43f90ceb609bebd092777b018ed29.ce5e2e07a9a4a04ba160adfc06fb4832
        #ZohoRecruit.modules.ALL
        #ZohoRecruit.users.ALL
        response = requests.post(token_url, data=data)
        if response.ok:
            tokens = response.json()
            tokens= self.generate_access_token_from_refresh_token(tokens.get('refresh_token'), client_id, client_secret)
            # Return as Django REST Response
            self.getCandidates= self.getCandidates(request,tokens)
            return Response(tokens, status=status.HTTP_200_OK)
            # print('Access Token:', tokens.get('access_token'))
            # print('Refresh Token:', tokens.get('refresh_token'))
        else:
            return Response({'error': response.text}, status=response.status_code)
            # print('Error:', response.status_code, response.text)
    

    def generate_access_token_from_refresh_token(self,refresh_token, client_id, client_secret):
        """
        Generate a new access token from a Zoho refresh token.
        Args:
            refresh_token (str): The Zoho OAuth2 refresh token.
            client_id (str): The Zoho client ID.
            client_secret (str): The Zoho client secret.
        Returns:
            dict: The response from Zoho containing the new access token or error info.
        """
        token_url = 'https://accounts.zoho.com/oauth/v2/token'
        payload = {
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token'
        }
        response = requests.post(token_url, data=payload)
        try:
            return response.json()
        except Exception:
            return {'error': 'Invalid response from Zoho.'}
    
    def getCandidates(self, request,token_resp):     
        access_token = token_resp.get('access_token')
        if not access_token:
                return Response({'error': 'Could not obtain access token from refresh token', 'zoho_response': token_resp}, status=status.HTTP_400_BAD_REQUEST)

        if not access_token:
            return Response({'error': 'No access token or refresh token found in config.'}, status=status.HTTP_400_BAD_REQUEST)

        # Zoho Recruit API endpoint for candidates
        candidates_url = 'https://recruit.zoho.com/recruit/v2/Candidates'
        headers = {
            'Authorization': f'Zoho-oauthtoken {access_token}'
        }
        response = requests.get(candidates_url, headers=headers)
        try:
            data = response.json()
        except Exception:
            return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
        if response.status_code == 200:
            return Response(data)
        return Response(data, status=response.status_code)
    

