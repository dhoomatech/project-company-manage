from django.urls import path
from .views import *

urlpatterns = [
    path('file-upload-64', FileUploadBase64.as_view()),
    path('file-upload', FileUpload.as_view()),
    path('service-request-send', ServicesRequestsCreate.as_view()),
    path('service-request-list', ServicesRequestsApproval.as_view()),
    path('my-service-request', MyServicesRequests.as_view()),
]
