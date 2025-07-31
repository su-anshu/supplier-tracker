# suppliers/admin.py
from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Enhanced Supplier Admin with all features"""
    
    list_display = [
        'supplier_id', 'supplier_name', 'contact_person', 'category', 
        'status', 'phone_number', 'email', 'credit_limit', 
        'has_bank_details', 'has_upi_scanner', 'get_items_count', 'get_transporters_count', 'created_at'
    ]
    
    list_filter = [
        'category', 'status', 'rating', 'payment_terms', 
        'created_at', 'updated_at'
    ]
    
    search_fields = [
        'supplier_name', 'supplier_id', 'contact_person', 
        'email', 'phone_number', 'city', 'gstin', 'pan_number'
    ]
    
    readonly_fields = ['supplier_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('supplier_id', 'supplier_name', 'contact_person', 'category', 'status', 'rating')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'alternate_phone', 'email', 'alternate_email', 'website')
        }),
        ('Address Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Business Information', {
            'fields': ('gstin', 'pan_number', 'payment_terms', 'credit_limit')
        }),
        ('Enhanced Features - Relationships', {
            'fields': ('items_supplied', 'preferred_transporters'),
            'classes': ('collapse',)
        }),
        ('Enhanced Features - Bank Information', {
            'fields': ('bank_name', 'account_number', 'ifsc_code', 'upi_scanner_image'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('products_services', 'remarks'),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_bank_details(self, obj):
        """Display if supplier has bank details"""
        return obj.has_bank_details
    has_bank_details.boolean = True
    has_bank_details.short_description = 'Bank Details'
    
    def has_upi_scanner(self, obj):
        """Display if supplier has UPI scanner"""
        return obj.has_upi_scanner
    has_upi_scanner.boolean = True
    has_upi_scanner.short_description = 'UPI Scanner'
    
    def get_items_count(self, obj):
        """Display count of items supplied"""
        return obj.items_supplied.count()
    get_items_count.short_description = 'Items'
    
    def get_transporters_count(self, obj):
        """Display count of preferred transporters"""
        return obj.preferred_transporters.count()
    get_transporters_count.short_description = 'Transporters'
