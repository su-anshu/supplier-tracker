# purchase_orders/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatusHistory,
    PurchaseOrderDocument
)


class PurchaseOrderItemInline(admin.TabularInline):
    """Inline for PO Items in admin"""
    model = PurchaseOrderItem
    extra = 1
    fields = [
        'item', 'quantity', 'unit_rate', 'line_total', 
        'tax_rate', 'tax_amount', 'line_total_with_tax'
    ]
    readonly_fields = ['line_total', 'tax_amount', 'line_total_with_tax']


class PurchaseOrderStatusHistoryInline(admin.TabularInline):
    """Inline for Status History in admin"""
    model = PurchaseOrderStatusHistory
    extra = 0
    readonly_fields = ['status', 'changed_at', 'changed_by', 'notes']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    """Enhanced admin for Purchase Orders"""
    
    list_display = [
        'po_number', 'supplier_link', 'po_date', 'total_amount',
        'status_badge', 'priority_badge', 'expected_delivery_date',
        'is_overdue_display', 'created_at'
    ]
    
    list_filter = [
        'status', 'priority', 'po_date', 'expected_delivery_date',
        'created_at', 'supplier'
    ]
    
    search_fields = [
        'po_number', 'supplier__supplier_name', 'reference_number',
        'delivery_contact_person'
    ]
    
    readonly_fields = [
        'po_number', 'subtotal', 'tax_amount', 'total_amount',
        'created_at', 'updated_at', 'approved_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'po_number', 'supplier', 'transporter', 'status', 'priority'
            )
        }),
        ('Dates', {
            'fields': (
                'po_date', 'expected_delivery_date', 'actual_delivery_date'
            )
        }),
        ('Financial', {
            'fields': (
                'payment_terms', 'discount_percentage', 'subtotal', 
                'tax_amount', 'total_amount'
            )
        }),
        ('Delivery Information', {
            'fields': (
                'delivery_address', 'delivery_contact_person', 'delivery_phone'
            )
        }),
        ('Additional Information', {
            'fields': (
                'reference_number', 'notes', 'terms_and_conditions'
            ),
            'classes': ('collapse',)
        }),
        ('Approval & Audit', {
            'fields': (
                'approved_by', 'approved_at', 'created_by', 
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PurchaseOrderItemInline, PurchaseOrderStatusHistoryInline]
    
    date_hierarchy = 'po_date'
    ordering = ['-created_at']
    
    def supplier_link(self, obj):
        """Create link to supplier detail"""
        url = reverse('admin:suppliers_supplier_change', args=[obj.supplier.pk])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.supplier_name)
    supplier_link.short_description = 'Supplier'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        color = obj.status_color
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        """Display priority as colored badge"""
        color = obj.priority_color
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def is_overdue_display(self, obj):
        """Display overdue status"""
        if obj.is_overdue:
            return format_html('<span class="text-danger">⚠️ Overdue</span>')
        return format_html('<span class="text-success">✓ On Time</span>')
    is_overdue_display.short_description = 'Delivery Status'
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related(
            'supplier', 'transporter'
        ).prefetch_related('items')


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    """Admin for PO Items"""
    
    list_display = [
        'purchase_order_link', 'item_link', 'quantity', 'unit_rate',
        'line_total_with_tax', 'received_quantity', 'pending_quantity',
        'delivery_status'
    ]
    
    list_filter = [
        'purchase_order__status', 'item__category',
        'expected_delivery_date', 'actual_delivery_date'
    ]
    
    search_fields = [
        'purchase_order__po_number', 'item__item_name', 'item__item_id'
    ]
    
    readonly_fields = [
        'line_total', 'tax_amount', 'line_total_with_tax', 'pending_quantity'
    ]
    
    def purchase_order_link(self, obj):
        """Link to PO"""
        url = reverse('admin:purchase_orders_purchaseorder_change', 
                     args=[obj.purchase_order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.purchase_order.po_number)
    purchase_order_link.short_description = 'Purchase Order'
    
    def item_link(self, obj):
        """Link to Item"""
        url = reverse('admin:items_item_change', args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', url, obj.item.item_name)
    item_link.short_description = 'Item'
    
    def delivery_status(self, obj):
        """Display delivery status"""
        if obj.is_fully_delivered:
            return format_html('<span class="text-success">✓ Delivered</span>')
        elif obj.received_quantity > 0:
            return format_html('<span class="text-warning">⚡ Partial</span>')
        else:
            return format_html('<span class="text-secondary">⏳ Pending</span>')
    delivery_status.short_description = 'Delivery'


@admin.register(PurchaseOrderStatusHistory)
class PurchaseOrderStatusHistoryAdmin(admin.ModelAdmin):
    """Admin for Status History"""
    
    list_display = [
        'purchase_order_link', 'status_badge', 'changed_at', 'changed_by'
    ]
    
    list_filter = ['status', 'changed_at']
    
    search_fields = ['purchase_order__po_number', 'changed_by']
    
    readonly_fields = ['purchase_order', 'status', 'changed_at', 'changed_by', 'notes']
    
    def purchase_order_link(self, obj):
        """Link to PO"""
        url = reverse('admin:purchase_orders_purchaseorder_change', 
                     args=[obj.purchase_order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.purchase_order.po_number)
    purchase_order_link.short_description = 'Purchase Order'
    
    def status_badge(self, obj):
        """Display status as badge"""
        return format_html(
            '<span class="badge badge-info">{}</span>',
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        """Disable manual adding - created automatically"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make read-only"""
        return False


@admin.register(PurchaseOrderDocument)
class PurchaseOrderDocumentAdmin(admin.ModelAdmin):
    """Admin for PO Documents"""
    
    list_display = [
        'purchase_order_link', 'document_type', 'description',
        'uploaded_at', 'uploaded_by'
    ]
    
    list_filter = ['document_type', 'uploaded_at']
    
    search_fields = ['purchase_order__po_number', 'description']
    
    readonly_fields = ['uploaded_at']
    
    def purchase_order_link(self, obj):
        """Link to PO"""
        url = reverse('admin:purchase_orders_purchaseorder_change', 
                     args=[obj.purchase_order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.purchase_order.po_number)
    purchase_order_link.short_description = 'Purchase Order'


# Customize admin site header
admin.site.site_header = "Mithila Foods - Purchase Order Management"
admin.site.site_title = "PO Management"
admin.site.index_title = "Purchase Order Administration"
