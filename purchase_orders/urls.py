# purchase_orders/urls.py
from django.urls import path
from . import views

app_name = 'purchase_orders'

urlpatterns = [
    # Main CRUD operations
    path('', views.PurchaseOrderListView.as_view(), name='po_list'),
    path('add/', views.create_purchase_order, name='po_add'),
    path('<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='po_detail'),
    path('<int:pk>/edit/', views.PurchaseOrderUpdateView.as_view(), name='po_edit'),
    path('<int:pk>/delete/', views.PurchaseOrderDeleteView.as_view(), name='po_delete'),
    
    # Status management actions
    path('<int:pk>/approve/', views.po_approve, name='po_approve'),
    path('<int:pk>/send-to-supplier/', views.po_send_to_supplier, name='po_send_to_supplier'),
    path('<int:pk>/mark-delivered/', views.po_mark_delivered, name='po_mark_delivered'),
    
    # Dashboard and analytics
    path('dashboard/', views.purchase_orders_dashboard, name='dashboard'),
    
    # AJAX endpoints
    path('ajax/item-details/', views.get_item_details, name='ajax_item_details'),
    path('ajax/supplier-details/', views.get_supplier_details, name='ajax_supplier_details'),
    path('ajax/search/', views.po_quick_search, name='po_search_ajax'),
    
    # Future endpoints for advanced features
    # path('<int:pk>/pdf/', views.generate_po_pdf, name='po_pdf'),
    # path('<int:pk>/email/', views.email_po_to_supplier, name='po_email'),
    # path('reports/', views.po_reports, name='po_reports'),
    # path('bulk-actions/', views.po_bulk_actions, name='po_bulk_actions'),
]
