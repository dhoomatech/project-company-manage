from django.urls import path
from . import views

urlpatterns = [
    path('createOrder/', views.createOrder),
    path('verifySignature/', views.verifySignature),

    path('transaction-list', views.TransactionList),
    path('transaction-from-list', views.TransactionFromList),
]