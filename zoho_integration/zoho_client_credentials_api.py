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


# --- Separate APIView subclasses for each endpoint ---

class ZohoAuthCodeTokenAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get Zoho access token using authorization code grant",
        manual_parameters=[
            openapi.Parameter('grant_token', openapi.IN_QUERY, description="Zoho grant token (authorization code)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('client_id', openapi.IN_QUERY, description="Zoho client ID",value="1000.KPFB56O12AVTZGSWB0WBMS5X2XI0LC",  type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('client_secret', openapi.IN_QUERY, description="Zoho client secret",value="9c39beb5ee700593f3a445505e235989c05720152a", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('redirect_uri', openapi.IN_QUERY, description="Redirect URI",value="http://localhost:8000", type=openapi.TYPE_STRING, required=True),
             openapi.Parameter('Scope', openapi.IN_QUERY, description="Scope",value="ZohoRecruit.modules.ALL", type=openapi.TYPE_STRING, required=True),
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
        grant_token = request.GET.get('grant_token')
        client_id = request.GET.get('client_id')
        client_secret = request.GET.get('client_secret')
        redirect_uri = request.GET.get('redirect_uri')
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
        except Exception:
            return Response({'error': 'Invalid response from Zoho.'}, status=status.HTTP_502_BAD_GATEWAY)
        if not response.ok or 'error' in tokens:
            return Response({'error': tokens.get('error', 'Failed to obtain token'), 'details': tokens}, status=response.status_code)
        # If refresh_token is present, exchange for access token
        if tokens.get('refresh_token'):
            payload = {
                'refresh_token': tokens.get('refresh_token'),
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'refresh_token'
            }
            try:
                resp2 = requests.post(token_url, data=payload)
                tokens2 = resp2.json()
            except Exception:
                return Response({'error': 'Invalid response from Zoho (refresh token).'}, status=status.HTTP_502_BAD_GATEWAY)
            if not resp2.ok or 'error' in tokens2:
                return Response({'error': tokens2.get('error', 'Failed to obtain access token from refresh token'), 'details': tokens2}, status=resp2.status_code)
            return Response(tokens2, status=status.HTTP_200_OK)
        return Response(tokens, status=status.HTTP_200_OK)

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
        refresh_token = request.data.get('refresh_token')
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')
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
            openapi.Parameter('candidate_id', openapi.IN_QUERY, description="Zoho candidate ID", type=openapi.TYPE_STRING, required=True)
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
        if not candidate_id:
            return Response({'error': 'candidate_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with open(API_CONFIG_PATH, 'r') as f:
                creds = json.load(f)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        access_token = creds.get('access_token')
        if not access_token and creds.get('refresh_token'):
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