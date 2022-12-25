from django.urls import path
# from . import views
from .views import *

urlpatterns = [
    path('membership-list', MembershipPackage.as_view()),
    path('admin/membership', MembershipPackageAdmin.as_view()),
    path('admin/membership-update', MembershipPackageAdminUpdate.as_view()),
    path('process', PaymentProcess.as_view()),
    path('process2', PaymentProcess2.as_view()),
    path('peyment-complete', PaymentSucess.as_view()),
    path('token-update', PaymentTokenUpdate.as_view()),
    
]