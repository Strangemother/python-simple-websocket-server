from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='sms-index'),
    path('receipt/', views.ReceiptView.as_view(), name='sms-receipt'),
    path('reply/', views.ReplyView.as_view(), name='sms-reply'),
]

