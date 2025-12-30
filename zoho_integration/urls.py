from django.urls import path
from .views import CandidateDetailAPI, CandidateResumeDownloadAPI, CandidateListAPI
from .zoho_client_credentials_api import (
    ZohoAuthCodeTokenAPIView,
    ZohoCandidateAttachmentListAPIView,
    ZohoRefreshTokenAPIView,
    ZohoCandidatesAPIView,
    ZohoResumeDownloadAPIView,
    ZohoCandidateAttachmentAPIView
)

urlpatterns = [
   # path('api/zoho/client-credentials-token/', ZohoClientCredentialsTokenAPIView.as_view(), name='zoho_client_credentials_token'),
    path('api/zoho/get-access-token/', ZohoAuthCodeTokenAPIView.as_view(), name='zoho_get_access_token'),
    path('api/zoho/get-access-token-param/', ZohoAuthCodeTokenAPIView.as_view(), name='zoho_get_access_token_param'),
    path('api/zoho/candidates/', ZohoCandidatesAPIView.as_view(), name='zoho_candidates'),
    path('api/zoho/candidate-resume/', ZohoResumeDownloadAPIView.as_view(), name='zoho_candidate_resume'),
    path('api/zoho/candidate-attachment/', ZohoCandidateAttachmentAPIView.as_view(), name='zoho_candidate_attachment'),
     path('api/zoho/candidate-attachment-list/', ZohoCandidateAttachmentListAPIView.as_view(), name='zoho_candidate_attachment_list'),
]
