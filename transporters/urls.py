# transporters/urls.py
from django.urls import path
from . import views

app_name = 'transporters'

urlpatterns = [
    # Professional Transporter CRUD operations
    path('', views.TransporterListView.as_view(), name='transporter_list'),
    path('add/', views.TransporterCreateView.as_view(), name='transporter_add'),
    path('<int:pk>/', views.TransporterDetailView.as_view(), name='transporter_detail'),
    path('<int:pk>/edit/', views.TransporterUpdateView.as_view(), name='transporter_edit'),
    path('<int:pk>/delete/', views.TransporterDeleteView.as_view(), name='transporter_delete'),
    
    # Dashboard
    path('dashboard/', views.transporters_dashboard, name='dashboard'),
    
    # AJAX endpoints
    path('ajax/search/', views.transporter_quick_search, name='transporter_search_ajax'),
    path('api/stats/', views.transporter_stats_api, name='transporter_stats_api'),
]
