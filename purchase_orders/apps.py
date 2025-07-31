# purchase_orders/apps.py
from django.apps import AppConfig


class PurchaseOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_orders'
    verbose_name = 'Purchase Orders'
