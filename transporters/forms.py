# transporters/forms.py
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Fieldset
from .models import (
    Transporter, TransporterStatus, VehicleType, RateType, TransporterRating
)
from suppliers.widgets import TransferWidget
from locations.models import City

class TransporterForm(ModelForm):
    """
    Professional Transporter Form with all compulsory and optional fields
    """
    
    class Meta:
        model = Transporter
        fields = [
            'transporter_name', 'contact_person', 'status',
            'phone_number', 'alternate_phone', 'email',
            'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country',
            'serviceable_cities', 'custom_locations',
            'primary_vehicle_type', 'fleet_size', 'vehicle_details',
            'rate_type', 'standard_rate', 'license_number', 'registration_number',
            'gstin', 'pan_number', 'rating', 'bank_name', 'account_number', 'ifsc_code', 
            'upi_scanner_image', 'services_offered', 'operational_hours', 'remarks'
        ]
        
        widgets = {
            'transporter_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter transporter/company name'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary contact person name'
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
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'transporter@company.com (optional)'
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
            'serviceable_cities': TransferWidget(),
            'custom_locations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Custom locations not in the city list (optional)'
            }),
            'primary_vehicle_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fleet_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': '1 (optional)'
            }),
            'vehicle_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Vehicle specifications, capacity, etc. (optional)'
            }),
            'rate_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'standard_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 (optional)'
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transport license number (optional)'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Business registration number (optional)'
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
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank name (optional)'
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank account number (optional)'
            }),
            'ifsc_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IFSC code (e.g., SBIN0001234) (optional)',
                'maxlength': '11',
                'style': 'text-transform: uppercase;'
            }),
            'upi_scanner_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'services_offered': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Types of transportation services offered (optional)'
            }),
            'operational_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 24/7, 9 AM - 6 PM (optional)'
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
        self.fields['serviceable_cities'].widget.choices = [
            (city.id, f"{city.name}, {city.state.name}") 
            for city in City.objects.exclude(name='Custom Location').order_by('name')
        ]
        
        # Set required fields (COMPULSORY FIELDS)
        required_fields = [
            'transporter_name', 'contact_person', 'phone_number',
            'address_line_1', 'city', 'state', 'postal_code'
        ]
        
        for field_name in required_fields:
            self.fields[field_name].required = True
        
        # Serviceable cities validation (at least one required)
        self.fields['serviceable_cities'].required = False  # Handle manually in clean method
            
        # Optional fields
        optional_fields = [
            'alternate_phone', 'email', 'address_line_2', 'primary_vehicle_type', 
            'fleet_size', 'vehicle_details', 'rate_type', 'standard_rate', 
            'license_number', 'registration_number', 'gstin', 'pan_number', 
            'bank_name', 'account_number', 'ifsc_code', 'upi_scanner_image', 
            'services_offered', 'operational_hours', 'remarks'
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
            HTML('<h5 class="mb-0"><i class="fas fa-truck"></i> Transporter Information</h5>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            # Basic Information Section
            Fieldset(
                'Basic Information',
                Row(
                    Column('transporter_name', css_class='form-group col-md-6 mb-3'),
                    Column('contact_person', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('status', css_class='form-group col-md-4 mb-3'),
                    Column('rating', css_class='form-group col-md-4 mb-3'),
                    Column('fleet_size', css_class='form-group col-md-4 mb-3'),
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
                'email',
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
            
            # Service Areas Section
            Fieldset(
                'Service Areas (Compulsory)',
                HTML('<div class="alert alert-warning">'),
                HTML('<i class="fas fa-map-marker-alt"></i> <strong>Compulsory:</strong> Select cities serviceable by this transporter.'),
                HTML('</div>'),
                'serviceable_cities',
                'custom_locations',
                css_class='mb-4'
            ),
            
            # Vehicle Information Section
            Fieldset(
                'Vehicle & Fleet Information (Optional)',
                HTML('<div class="alert alert-info">'),
                HTML('<i class="fas fa-info-circle"></i> <strong>Note:</strong> All vehicle and rate fields are now optional.'),
                HTML('</div>'),
                Row(
                    Column('primary_vehicle_type', css_class='form-group col-md-6 mb-3'),
                    Column('rate_type', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('fleet_size', css_class='form-group col-md-6 mb-3'),
                    Column('standard_rate', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('operational_hours', css_class='form-group col-md-12 mb-3'),
                    css_class='form-row'
                ),
                'vehicle_details',
                'services_offered',
                css_class='mb-4'
            ),
            
            # Business Information Section
            Fieldset(
                'Business & License Information (Optional)',
                Row(
                    Column('license_number', css_class='form-group col-md-6 mb-3'),
                    Column('registration_number', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column('gstin', css_class='form-group col-md-6 mb-3'),
                    Column('pan_number', css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                css_class='mb-4'
            ),
            
            # Payment Details Section
            Fieldset(
                'Payment Details (Optional)',
                HTML('<div class="alert alert-info">'),
                HTML('<i class="fas fa-info-circle"></i> <strong>Payment Information:</strong> Bank details and UPI scanner for payment processing.'),
                HTML('</div>'),
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
                'Additional Information',
                'remarks',
                css_class='mb-4'
            ),
            
            HTML('</div>'),
            HTML('</div>'),
            
            Div(
                Submit('submit', 'Save Transporter', css_class='btn btn-success btn-lg me-2'),
                HTML('<a href="{% url "transporters:transporter_list" %}" class="btn btn-secondary btn-lg">Cancel</a>'),
                css_class='d-flex justify-content-center mt-4'
            )
        )
        
        # Add required field indicators
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
    
    def clean(self):
        """Custom validation to ensure at least one serviceable location"""
        cleaned_data = super().clean()
        
        # Check if serviceable cities are provided
        serviceable_cities_data = self.data.get('serviceable_cities', '')
        custom_locations = cleaned_data.get('custom_locations', '')
        
        # At least one type of location must be provided
        if not serviceable_cities_data and not custom_locations:
            raise forms.ValidationError(
                "Please provide at least one serviceable location (either select cities or enter custom locations)."
            )
        
        return cleaned_data
    
    def clean_transporter_name(self):
        """Ensure transporter name is unique (case-insensitive)"""
        transporter_name = self.cleaned_data.get('transporter_name')
        if transporter_name:
            transporter_name = transporter_name.strip()
            existing_transporter = Transporter.objects.filter(
                transporter_name__iexact=transporter_name
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_transporter.exists():
                raise forms.ValidationError(
                    "A transporter with this name already exists."
                )
        return transporter_name
    
    def clean_serviceable_locations_text(self):
        """Validate serviceable locations text format"""
        locations = self.cleaned_data.get('serviceable_locations_text')
        if locations:
            locations = locations.strip()
            # Basic validation - ensure it's not empty after stripping
            if not locations:
                raise forms.ValidationError(
                    "Please enter at least one serviceable location."
                )
        return locations
    
    def clean_gstin(self):
        """Validate GSTIN format if provided"""
        gstin = self.cleaned_data.get('gstin')
        if gstin:
            gstin = gstin.strip().upper()
            # Check uniqueness
            existing_transporter = Transporter.objects.filter(
                gstin=gstin
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_transporter.exists():
                raise forms.ValidationError(
                    "A transporter with this GSTIN already exists."
                )
        return gstin
    
    def clean_pan_number(self):
        """Validate PAN number format if provided"""
        pan_number = self.cleaned_data.get('pan_number')
        if pan_number:
            pan_number = pan_number.strip().upper()
            # Check uniqueness
            existing_transporter = Transporter.objects.filter(
                pan_number=pan_number
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_transporter.exists():
                raise forms.ValidationError(
                    "A transporter with this PAN number already exists."
                )
        return pan_number
    
    def clean_ifsc_code(self):
        """Validate IFSC code format if provided"""
        ifsc_code = self.cleaned_data.get('ifsc_code')
        if ifsc_code:
            ifsc_code = ifsc_code.strip().upper()
        return ifsc_code
    
    def save(self, commit=True):
        """Custom save method to handle ManyToMany fields from TransferWidget"""
        instance = super().save(commit=commit)
        
        if commit:
            # Handle serviceable_cities from TransferWidget
            serviceable_cities_data = self.data.get('serviceable_cities', '')
            if serviceable_cities_data:
                city_ids = [int(id_str) for id_str in serviceable_cities_data.split(',') if id_str.strip()]
                instance.serviceable_cities.set(city_ids)
            else:
                instance.serviceable_cities.clear()
        
        return instance

class TransporterSearchForm(forms.Form):
    """
    Form for searching and filtering transporters
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, ID, contact person, location...',
            'autofocus': True
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + list(TransporterStatus.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    vehicle_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Vehicle Types')] + list(VehicleType.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    rating = forms.ChoiceField(
        required=False,
        choices=[('', 'All Ratings')] + list(TransporterRating.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # ENHANCED FILTERING
    services_city = forms.ModelChoiceField(
        required=False,
        queryset=City.objects.exclude(name='Custom Location').order_by('name'),
        empty_label="Filter by City Serviced",
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
            HTML('<h6 class="mb-0"><i class="fas fa-search"></i> Search & Filter Transporters</h6>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('search', css_class='form-group col-md-4 mb-3'),
                Column('status', css_class='form-group col-md-2 mb-3'),
                Column('vehicle_type', css_class='form-group col-md-2 mb-3'),
                Column('rating', css_class='form-group col-md-2 mb-3'),
                Column('services_city', css_class='form-group col-md-2 mb-3'),
                css_class='form-row'
            ),
            
            Div(
                Submit('filter', 'Apply Filters', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "transporters:transporter_list" %}" class="btn btn-outline-secondary">Clear</a>'),
                css_class='text-center'
            ),
            
            HTML('</div>'),
            HTML('</div>'),
        )
