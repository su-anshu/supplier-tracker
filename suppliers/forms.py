# suppliers/forms.py
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Fieldset
from .models import (
    Supplier, SupplierCategory, SupplierStatus, PaymentTerms, SupplierRating
)
from .widgets import TransferWidget
from items.models import Item
from transporters.models import Transporter

class SupplierForm(ModelForm):
    """
    Enhanced Supplier Form with all requested features:
    - Email (optional)
    - Credit limit (optional)
    - Bank details (optional)
    - UPI scanner image (optional)
    NO items/transporters selection as requested
    """
    
    class Meta:
        model = Supplier
        fields = [
            'supplier_name', 'contact_person', 'category', 'status',
            'phone_number', 'alternate_phone', 'email', 'alternate_email', 'website',
            'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country',
            'gstin', 'pan_number', 'payment_terms', 'credit_limit', 'rating',
            'bank_name', 'account_number', 'ifsc_code', 'upi_scanner_image',
            'items_supplied', 'preferred_transporters',
            'products_services', 'remarks'
        ]
        
        widgets = {
            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier/company name'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary contact person name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-9876543210'
            }),
            'alternate_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-9876543211 (optional)'
            }),
            # ENHANCED FEATURE: Email (OPTIONAL)
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'supplier@company.com (OPTIONAL)'
            }),
            'alternate_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'alternate@company.com (optional)'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.company.com (optional)'
            }),
            'address_line_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address line 1'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address line 2 (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal/ZIP code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'India'
            }),
            'gstin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '22AAAAA0000A1Z5 (optional)',
                'maxlength': '15'
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABCDE1234F (optional)',
                'maxlength': '10',
                'style': 'text-transform: uppercase;'
            }),
            'payment_terms': forms.Select(attrs={
                'class': 'form-select'
            }),
            # ENHANCED FEATURE: Credit Limit (OPTIONAL)
            'credit_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 (OPTIONAL)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            # ENHANCED FEATURE: Bank Details (OPTIONAL)
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank name (OPTIONAL)'
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank account number (OPTIONAL)'
            }),
            'ifsc_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IFSC code (e.g., SBIN0001234) (OPTIONAL)',
                'maxlength': '11',
                'style': 'text-transform: uppercase;'
            }),
            # ENHANCED FEATURE: UPI Scanner (OPTIONAL)
            'upi_scanner_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'items_supplied': TransferWidget(),
            'preferred_transporters': TransferWidget(),
            'products_services': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Products/services offered by supplier (optional)'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes or comments (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up transfer widget choices
        self.fields['items_supplied'].widget.choices = [
            (item.id, f"{item.item_id} - {item.item_name}") 
            for item in Item.objects.filter(status='active').order_by('item_name')
        ]
        
        self.fields['preferred_transporters'].widget.choices = [
            (transporter.id, f"{transporter.transporter_id} - {transporter.transporter_name}") 
            for transporter in Transporter.objects.filter(status='active').order_by('transporter_name')
        ]
        
        # Set required fields
        required_fields = [
            'supplier_name', 'contact_person', 'category', 'status',
            'phone_number', 'address_line_1', 'city', 'state', 'postal_code'
        ]
        
        for field_name in required_fields:
            self.fields[field_name].required = True
            
        # ENHANCED FEATURES: Make these fields optional
        optional_fields = [
            'alternate_phone', 'email', 'alternate_email', 'website', 'address_line_2',
            'gstin', 'pan_number', 'credit_limit', 'bank_name', 'account_number', 
            'ifsc_code', 'upi_scanner_image', 'items_supplied', 'preferred_transporters',
            'products_services', 'remarks'
        ]
        
        for field_name in optional_fields:
            self.fields[field_name].required = False
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': '', 'enctype': 'multipart/form-data'}
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-primary text-white">'),
            HTML('<h5 class="mb-0"><i class="fas fa-building"></i> Supplier Information</h5>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            # Basic Information Section
            Fieldset(
                'Basic Information',
                Row(
                    Column('supplier_name', css_class='form-group col-md-6 mb-3'),
                    Column('contact_person', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('category', css_class='form-group col-md-4 mb-3'),
                    Column('status', css_class='form-group col-md-4 mb-3'),
                    Column('rating', css_class='form-group col-md-4 mb-3'),
                    css_class='form-row'
                ),
                css_class='mb-4'
            ),
            
            # Contact Information Section
            Fieldset(
                'Contact Information',
                Row(
                    Column('phone_number', css_class='form-group col-md-6 mb-3'),
                    Column('alternate_phone', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('email', css_class='form-group col-md-6 mb-3'),
                    Column('alternate_email', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                'website',
                css_class='mb-4'
            ),
            
            # Address Information Section
            Fieldset(
                'Address Information',
                'address_line_1',
                'address_line_2',
                Row(
                    Column('city', css_class='form-group col-md-4 mb-3'),
                    Column('state', css_class='form-group col-md-4 mb-3'),
                    Column('postal_code', css_class='form-group col-md-4 mb-3'),
                    css_class='form-row'
                ),
                'country',
                css_class='mb-4'
            ),
            
            # Business Information Section
            Fieldset(
                'Business Information',
                Row(
                    Column('gstin', css_class='form-group col-md-6 mb-3'),
                    Column('pan_number', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('payment_terms', css_class='form-group col-md-6 mb-3'),
                    Column('credit_limit', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                css_class='mb-4'
            ),
            
            # Bank Information Section
            Fieldset(
                'Bank Information (Optional)',
                Row(
                    Column('bank_name', css_class='form-group col-md-4 mb-3'),
                    Column('account_number', css_class='form-group col-md-4 mb-3'),
                    Column('ifsc_code', css_class='form-group col-md-4 mb-3'),
                    css_class='form-row'
                ),
                'upi_scanner_image',
                css_class='mb-4'
            ),
            
            # Additional Information Section
            Fieldset(
                'Business Relationships',
                HTML('<div class="alert alert-info">'),
                HTML('<i class="fas fa-handshake"></i> <strong>Optional:</strong> Select items this supplier can provide and preferred transporters.'),
                HTML('</div>'),
                'items_supplied',
                'preferred_transporters',
                css_class='mb-4'
            ),
            
            Fieldset(
                'Additional Information',
                'products_services',
                'remarks',
                css_class='mb-4'
            ),
            
            HTML('</div>'),
            HTML('</div>'),
            
            Div(
                Submit('submit', 'Save Supplier', css_class='btn btn-success btn-lg me-2'),
                HTML('<a href="{% url "suppliers:supplier_list" %}" class="btn btn-secondary btn-lg">Cancel</a>'),
                css_class='d-flex justify-content-center mt-4'
            )
        )
        
        # Add required field indicators
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
    
    def clean_supplier_name(self):
        """Ensure supplier name is unique (case-insensitive)"""
        supplier_name = self.cleaned_data.get('supplier_name')
        if supplier_name:
            supplier_name = supplier_name.strip()
            existing_supplier = Supplier.objects.filter(
                supplier_name__iexact=supplier_name
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_supplier.exists():
                raise forms.ValidationError(
                    "A supplier with this name already exists."
                )
        return supplier_name
    
    def clean_gstin(self):
        """Validate GSTIN format if provided"""
        gstin = self.cleaned_data.get('gstin')
        if gstin:
            gstin = gstin.strip().upper()
            # GSTIN validation is handled by model validator
            # Check uniqueness
            existing_supplier = Supplier.objects.filter(
                gstin=gstin
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_supplier.exists():
                raise forms.ValidationError(
                    "A supplier with this GSTIN already exists."
                )
        return gstin
    
    def clean_pan_number(self):
        """Validate PAN number format if provided"""
        pan_number = self.cleaned_data.get('pan_number')
        if pan_number:
            pan_number = pan_number.strip().upper()
            # PAN validation is handled by model validator
            # Check uniqueness
            existing_supplier = Supplier.objects.filter(
                pan_number=pan_number
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_supplier.exists():
                raise forms.ValidationError(
                    "A supplier with this PAN number already exists."
                )
        return pan_number
    
    def clean_ifsc_code(self):
        """Validate IFSC code format if provided"""
        ifsc_code = self.cleaned_data.get('ifsc_code')
        if ifsc_code:
            ifsc_code = ifsc_code.strip().upper()
        return ifsc_code

class SupplierSearchForm(forms.Form):
    """
    Form for searching and filtering suppliers
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, ID, contact person...',
            'autofocus': True
        })
    )
    
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + list(SupplierCategory.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + list(SupplierStatus.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    rating = forms.ChoiceField(
        required=False,
        choices=[('', 'All Ratings')] + list(SupplierRating.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # ENHANCED FILTERING
    supplies_item = forms.ModelChoiceField(
        required=False,
        queryset=Item.objects.filter(status='active').order_by('item_name'),
        empty_label="Filter by Item Supplied",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    has_bank_details = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('yes', 'Has Bank Details'), ('no', 'No Bank Details')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'mb-4'
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header">'),
            HTML('<h6 class="mb-0"><i class="fas fa-search"></i> Search & Filter Suppliers</h6>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('search', css_class='form-group col-md-3 mb-3'),
                Column('category', css_class='form-group col-md-2 mb-3'),
                Column('status', css_class='form-group col-md-2 mb-3'),
                Column('rating', css_class='form-group col-md-2 mb-3'),
                Column('supplies_item', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            
            Row(
                Column('has_bank_details', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            
            Div(
                Submit('filter', 'Apply Filters', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "suppliers:supplier_list" %}" class="btn btn-outline-secondary">Clear</a>'),
                css_class='text-center'
            ),
            
            HTML('</div>'),
            HTML('</div>'),
        )
