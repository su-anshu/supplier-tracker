# transporters/admin.py
from django.contrib import admin
from .models import Transporter

@admin.register(Transporter)
class TransporterAdmin(admin.ModelAdmin):
    """Professional Transporter Admin"""
    
    list_display = [
        'transporter_id', 'transporter_name', 'contact_person', 'status', 
        'phone_number', 'email', 'primary_vehicle_type', 'fleet_size',
        'rating', 'has_business_details', 'has_payment_details', 'has_upi_scanner', 
        'get_items_count', 'get_districts_count', 'created_at'
    ]
    
    list_filter = [
        'status', 'primary_vehicle_type', 'rating', 'rate_type',
        'created_at', 'updated_at'
    ]
    
    search_fields = [
        'transporter_name', 'transporter_id', 'contact_person', 
        'email', 'phone_number', 'city', 'serviceable_locations',
        'gstin', 'pan_number', 'license_number'
    ]
    
    readonly_fields = ['transporter_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('transporter_id', 'transporter_name', 'contact_person', 'status', 'rating')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'alternate_phone', 'email')
        }),
        ('Address Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Service Areas (Compulsory)', {
            'fields': ('serviceable_locations',)
        }),
        ('Vehicle & Fleet Information', {
            'fields': ('primary_vehicle_type', 'fleet_size', 'vehicle_details', 'rate_type', 'standard_rate', 'operational_hours')
        }),
        ('Business Information', {
            'fields': ('license_number', 'registration_number', 'gstin', 'pan_number'),
            'classes': ('collapse',)
        }),
        ('Payment Information', {
            'fields': ('bank_name', 'account_number', 'ifsc_code', 'upi_scanner_image'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('services_offered', 'remarks'),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_business_details(self, obj):
        """Display if transporter has business details"""
        return obj.has_business_details
    has_business_details.boolean = True
    has_business_details.short_description = 'Business Details'
    
    def has_payment_details(self, obj):
        """Display if transporter has payment details"""
        return obj.has_payment_details
    has_payment_details.boolean = True
    has_payment_details.short_description = 'Payment Details'
    
    def has_upi_scanner(self, obj):
        """Display if transporter has UPI scanner"""
        return obj.has_upi_scanner
    has_upi_scanner.boolean = True
    has_upi_scanner.short_description = 'UPI Scanner'
    
    def get_items_count(self, obj):
        """Display count of items carried"""
        return obj.items_carried.count()
    get_items_count.short_description = 'Items'
    
    def get_districts_count(self, obj):
        """Display count of serviceable districts"""  
        return obj.serviceable_districts.count()
    get_districts_count.short_description = 'Districts'
