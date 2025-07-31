# items/forms.py
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from .models import Item, ItemCategory, ItemStatus

# Common unit choices for the dropdown
UNIT_CHOICES = [
    ('', 'Select Unit'),
    ('kg', 'Kilogram (kg)'),
    ('grams', 'Grams'),
    ('liters', 'Liters'),
    ('ml', 'Milliliters'),
    ('pcs', 'Pieces'),
    ('boxes', 'Boxes'),
    ('rolls', 'Rolls'),
    ('meters', 'Meters'),
    ('feet', 'Feet'),
    ('bags', 'Bags'),
]

class ItemForm(ModelForm):
    """
    Simplified form for adding/editing items
    """
    
    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='Select the unit of measurement'
    )
    
    class Meta:
        model = Item
        fields = [
            'item_name', 'status', 'category', 'unit', 'hsn_code', 'tax_rate',
            'reorder_level', 'standard_rate', 'shelf_life_days',
            'specification', 'description', 'remarks'
        ]
        
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item name'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hsn_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1006, 4819 (optional)'
            }),
            'tax_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'value': '18.00'
            }),
            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'standard_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'shelf_life_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Leave empty if not applicable'
            }),
            'specification': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quality specifications, size, color, etc. (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed description of the item (optional)'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes or comments (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set required fields
        self.fields['item_name'].required = True
        self.fields['status'].required = True
        self.fields['category'].required = True
        self.fields['unit'].required = True
        
        # Make other fields optional
        self.fields['hsn_code'].required = False
        self.fields['tax_rate'].required = False
        self.fields['reorder_level'].required = False
        self.fields['standard_rate'].required = False
        self.fields['shelf_life_days'].required = False
        self.fields['specification'].required = False
        self.fields['description'].required = False
        self.fields['remarks'].required = False
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-primary text-white">'),
            HTML('<h5 class="mb-0"><i class="fas fa-box"></i> Item Information</h5>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            HTML('<h6 class="text-primary mb-3">Required Information</h6>'),
            Row(
                Column('item_name', css_class='form-group col-md-6 mb-3'),
                Column('status', css_class='form-group col-md-3 mb-3'),
                Column('category', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            
            Row(
                Column('unit', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<hr class="my-4">'),
            HTML('<h6 class="text-secondary mb-3">Optional Information</h6>'),
            
            Row(
                Column('hsn_code', css_class='form-group col-md-4 mb-3'),
                Column('tax_rate', css_class='form-group col-md-4 mb-3'),
                Column('reorder_level', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            
            Row(
                Column('standard_rate', css_class='form-group col-md-6 mb-3'),
                Column('shelf_life_days', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            'specification',
            'description',
            'remarks',
            
            HTML('</div>'),
            HTML('</div>'),
            
            Div(
                Submit('submit', 'Save Item', css_class='btn btn-success btn-lg me-2'),
                HTML('<a href="{% url "items:item_list" %}" class="btn btn-secondary btn-lg">Cancel</a>'),
                css_class='d-flex justify-content-center mt-4'
            )
        )
        
        # Add required field indicators
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
    
    def clean_item_name(self):
        """Ensure item name is unique (case-insensitive)"""
        item_name = self.cleaned_data.get('item_name')
        if item_name:
            item_name = item_name.strip()
            existing_item = Item.objects.filter(
                item_name__iexact=item_name
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_item.exists():
                raise forms.ValidationError(
                    "An item with this name already exists."
                )
        return item_name

class ItemSearchForm(forms.Form):
    """
    Form for searching and filtering items
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by item name or ID...',
            'autofocus': True
        })
    )
    
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + list(ItemCategory.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + list(ItemStatus.choices),
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
            HTML('<h6 class="mb-0"><i class="fas fa-search"></i> Search & Filter Items</h6>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('search', css_class='form-group col-md-6 mb-3'),
                Column('category', css_class='form-group col-md-3 mb-3'),
                Column('status', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            
            Div(
                Submit('filter', 'Apply Filters', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "items:item_list" %}" class="btn btn-outline-secondary">Clear</a>'),
                css_class='text-center'
            ),
            
            HTML('</div>'),
            HTML('</div>'),
        )
class BulkUploadForm(forms.Form):
    """
    Form for bulk uploading items via Excel file
    """
    excel_file = forms.FileField(
        label='Excel File',
        help_text='Upload Excel file (.xlsx or .xls) with item data',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'needs-validation'
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-success text-white">'),
            HTML('<h5 class="mb-0"><i class="fas fa-file-excel"></i> Bulk Upload Items</h5>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            HTML('<div class="alert alert-info">'),
            HTML('<h6><i class="fas fa-info-circle"></i> Instructions:</h6>'),
            HTML('<ul class="mb-0">'),
            HTML('<li><strong>Required columns:</strong> item_name, category, unit, status</li>'),
            HTML('<li><strong>Optional columns:</strong> hsn_code, tax_rate, reorder_level, standard_rate, shelf_life_days, specification, description, remarks</li>'),
            HTML('<li><strong>Valid categories:</strong> raw_material, packaging, stationery, infrastructure, others</li>'),
            HTML('<li><strong>Valid units:</strong> kg, grams, liters, ml, pcs, boxes, rolls, meters, feet, bags</li>'),
            HTML('<li><strong>Valid status:</strong> active, inactive, discontinued</li>'),
            HTML('<li>Download the template below to see the exact format</li>'),
            HTML('</ul>'),
            HTML('</div>'),
            
            'excel_file',
            
            HTML('<div class="mt-3">'),
            HTML('<a href="{% url "items:download_template" %}" class="btn btn-outline-primary me-2">'),
            HTML('<i class="fas fa-download"></i> Download Template'),
            HTML('</a>'),
            HTML('</div>'),
            
            HTML('</div>'),
            HTML('</div>'),
            
            Div(
                Submit('submit', 'Upload Items', css_class='btn btn-success btn-lg me-2'),
                HTML('<a href="{% url "items:item_list" %}" class="btn btn-secondary btn-lg">Cancel</a>'),
                css_class='d-flex justify-content-center mt-4'
            )
        )
    
    def clean_excel_file(self):
        """Validate the uploaded file"""
        excel_file = self.cleaned_data.get('excel_file')
        
        if excel_file:
            # Check file extension
            if not excel_file.name.lower().endswith(('.xlsx', '.xls')):
                raise forms.ValidationError(
                    'Please upload a valid Excel file (.xlsx or .xls)'
                )
            
            # Check file size (max 5MB)
            if excel_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'File size too large. Maximum size is 5MB.'
                )
        
        return excel_file


# Transfer Widget Forms
class ItemTransferForm(forms.Form):
    """Form for transferring items between locations or processes"""
    item = forms.ModelChoiceField(
        queryset=Item.objects.filter(status='active'),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'transfer-item-select'
        }),
        help_text="Select the item to transfer"
    )
    quantity = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter quantity'
        }),
        help_text="Quantity to transfer"
    )
    from_location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'From Location'
        }),
        help_text="Source location"
    )
    to_location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'To Location'
        }),
        help_text="Destination location"
    )
    transfer_reason = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Reason for transfer (optional)'
        }),
        help_text="Optional reason for the transfer"
    )
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional remarks (optional)'
        }),
        required=False,
        help_text="Any additional notes"
    )

class BulkItemSelectForm(forms.Form):
    """Form for bulk item selection"""
    selected_items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.filter(status='active'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        help_text="Select items for bulk operations"
    )
    action = forms.ChoiceField(
        choices=[
            ('transfer', 'Transfer Items'),
            ('activate', 'Activate Items'),
            ('deactivate', 'Deactivate Items'),
            ('export', 'Export Selected Items')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Choose action to perform on selected items"
    )
