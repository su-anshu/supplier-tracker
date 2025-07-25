# items/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Item, ItemSupplier

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Item model
    """
    list_display = [
        'item_id', 'item_name', 'category', 'status_colored', 
        'standard_rate_formatted', 'tax_rate', 'reorder_level', 'created_at'
    ]
    
    list_filter = [
        'category', 'status', 'tax_rate',
        'created_at', 'updated_at'
    ]
    
    search_fields = [
        'item_name', 'item_id', 'hsn_code', 'specification', 'description'
    ]
    
    readonly_fields = ['item_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_id', 'item_name', 'category', 'unit', 'status')
        }),
        ('Tax & Compliance', {
            'fields': ('hsn_code', 'tax_rate'),
            'classes': ('collapse',)
        }),
        ('Inventory Management', {
            'fields': (
                'reorder_level', 'standard_rate', 'shelf_life_days'
            ),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('specification', 'description', 'remarks'),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    actions = ['activate_items', 'deactivate_items', 'discontinue_items']
    
    def status_colored(self, obj):
        """Display status with color coding"""
        colors = {
            'active': 'green',
            'inactive': 'orange', 
            'discontinued': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
    
    def standard_rate_formatted(self, obj):
        """Display standard rate with currency formatting"""
        if obj.standard_rate:
            return f"₹{obj.standard_rate:,.2f}"
        return "-"
    standard_rate_formatted.short_description = 'Standard Rate'
    standard_rate_formatted.admin_order_field = 'standard_rate'
    
    def activate_items(self, request, queryset):
        """Bulk activate items"""
        updated = queryset.update(status='active')
        self.message_user(
            request,
            f'{updated} items were successfully activated.'
        )
    activate_items.short_description = 'Activate selected items'
    
    def deactivate_items(self, request, queryset):
        """Bulk deactivate items"""
        updated = queryset.update(status='inactive')
        self.message_user(
            request,
            f'{updated} items were successfully deactivated.'
        )
    deactivate_items.short_description = 'Deactivate selected items'
    
    def discontinue_items(self, request, queryset):
        """Bulk discontinue items"""
        updated = queryset.update(status='discontinued')
        self.message_user(
            request,
            f'{updated} items were successfully discontinued.'
        )
    discontinue_items.short_description = 'Discontinue selected items'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related()

@admin.register(ItemSupplier)
class ItemSupplierAdmin(admin.ModelAdmin):
    """
    Admin interface for Item Supplier mapping
    """
    list_display = [
        'item', 'supplier_name', 'preference_order', 
        'last_rate_formatted', 'is_active', 'created_at'
    ]
    
    list_filter = ['is_active', 'preference_order', 'created_at']
    search_fields = ['item__item_name', 'supplier_name']
    list_editable = ['preference_order', 'is_active']
    
    ordering = ['item__item_name', 'preference_order']
    
    def last_rate_formatted(self, obj):
        """Display last rate with currency formatting"""
        if obj.last_rate:
            return f"₹{obj.last_rate:,.2f}"
        return "-"
    last_rate_formatted.short_description = 'Last Rate'
    last_rate_formatted.admin_order_field = 'last_rate'

# Customize admin site
admin.site.site_header = "Mithila Foods - Supplier Tracker Admin"
admin.site.site_title = "Supplier Tracker Admin"
admin.site.index_title = "Welcome to Supplier Tracker Administration"
