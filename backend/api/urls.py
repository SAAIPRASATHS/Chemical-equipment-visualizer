"""
API URL configuration.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register_user, name='register'),
    
    # Data management endpoints
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/', views.get_summary, name='get_summary'),
    path('history/', views.get_history, name='get_history'),
    path('dataset/<int:dataset_id>/', views.get_dataset_detail, name='dataset_detail'),
    
    # Report generation
    path('report/<int:dataset_id>/', views.generate_report, name='generate_report'),
]
