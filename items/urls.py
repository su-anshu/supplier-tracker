# items/urls.py
from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    # Main CRUD operations
    path('', views.ItemListView.as_view(), name='item_list'),
    path('add/', views.ItemCreateView.as_view(), name='item_add'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # Bulk upload
    path('bulk-upload/', views.bulk_upload_view, name='bulk_upload'),
    path('bulk-upload/results/', views.bulk_upload_results, name='bulk_upload_results'),
    path('download-template/', views.download_template, name='download_template'),
    
    # Dashboard and analytics
    path('dashboard/', views.items_dashboard, name='dashboard'),
    
    # API endpoints
    path('api/by-category/', views.item_category_view, name='api_by_category'),
    path('api/search/', views.item_search_api, name='api_search'),
    
    # Bulk operations
    path('bulk-update/', views.bulk_update_items, name='bulk_update'),
]
