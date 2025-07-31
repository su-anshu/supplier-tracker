# suppliers/urls.py
from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    # Enhanced Supplier CRUD operations
    path('', views.SupplierListView.as_view(), name='supplier_list'),
    path('add/', views.SupplierCreateView.as_view(), name='supplier_add'),
    path('<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_edit'),
    path('<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Enhanced Dashboard
    path('dashboard/', views.suppliers_dashboard, name='dashboard'),
    
    # AJAX endpoints
    path('ajax/search/', views.supplier_quick_search, name='supplier_search_ajax'),
    path('api/stats/', views.supplier_stats_api, name='supplier_stats_api'),
]
