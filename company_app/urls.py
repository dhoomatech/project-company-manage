from django.urls import path
from .views import *

urlpatterns = [
    path('file-upload-64', FileUploadBase64.as_view()),
    path('file-upload', FileUpload.as_view()),
    path('file-upload-delete/<int:file_id>', FileDelete.as_view()),
    path('file-update/<int:file_id>', FileUpdate.as_view()),

    path('service-request-send', ServicesRequestsCreate.as_view()),
    path('service-request-list', ServicesRequestsApprovalList.as_view()),
    path('my-service-request', MyServicesRequests.as_view()),
    path('my-notifications', NotificationList.as_view()),
    path('manager-service-create', ServicesManagerCreate.as_view()),
    path('manager-service-list', CompanyManagerServiceList.as_view()),

    path('manager-service-approval/<int:service_id>', ServicesRequestsApproval.as_view()),

    path('dashboard', Dashboard.as_view()),

    path('folder-update', FolderFileUpdate.as_view()),

    path('privacy-policy', PrivacyPolicy.as_view()),


]
