from django.urls import path
from .views import CandidateDetailAPI, CandidateResumeDownloadAPI, CandidateListAPI
from .zoho_oauth_api import ZohoOAuthTokenAPI
from .zoho_client_credentials_api import ZohoClientCredentialsTokenAPI

urlpatterns = [
    path('api/candidates/', CandidateListAPI.as_view(), name='zoho_candidate_list'),
    path('api/candidate/<str:candidate_id>/', CandidateDetailAPI.as_view(), name='zoho_candidate_detail'),
    path('api/candidate/<str:candidate_id>/resume/', CandidateResumeDownloadAPI.as_view(), name='zoho_candidate_resume_download'),
    path('api/zoho/oauth-token/', ZohoOAuthTokenAPI.as_view(), name='zoho_oauth_token'),
    path('api/zoho/client-credentials-token/', ZohoClientCredentialsTokenAPI.as_view(), name='zoho_client_credentials_token'),
]
