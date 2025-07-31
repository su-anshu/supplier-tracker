# purchase_orders/forms.py
from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field
from decimal import Decimal
from datetime import date, timedelta

from .models import (
    PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus, 
    PurchaseOrderPriority, PaymentTerms
)
from items.models import Item
from suppliers.models import Supplier
from transporters.models import Transporter


class PurchaseOrderForm(forms.ModelForm):
    """
    Enhanced form for creating/editing Purchase Orders
    """
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'supplier', 'transporter', 'po_date', 'expected_delivery_date',
            'priority', 'payment_terms', 'delivery_address', 
            'delivery_contact_person', 'delivery_phone', 'reference_number',
            'discount_percentage', 'notes', 'terms_and_conditions'
        ]
        
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_supplier'
            }),
            'transporter': forms.Select(attrs={
                'class': 'form-select'
            }),
            'po_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expected_delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'payment_terms': forms.Select(attrs={
                'class': 'form-select'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Complete delivery address'
            }),
            'delivery_contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            'delivery_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 9876543210'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'External reference number (optional)'
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'value': '0.00'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes or instructions (optional)'
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Terms and conditions (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter active suppliers and transporters
        self.fields['supplier'].queryset = Supplier.objects.filter(status='active').order_by('supplier_name')
        self.fields['transporter'].queryset = Transporter.objects.filter(status='active').order_by('transporter_name')
        
        # Set required fields
        self.fields['supplier'].required = True
        self.fields['po_date'].required = True
        self.fields['expected_delivery_date'].required = True
        self.fields['delivery_address'].required = True
        self.fields['delivery_contact_person'].required = True
        self.fields['delivery_phone'].required = True
        
        # Set default values
        if not self.instance.pk:  # Only for new POs
            self.fields['po_date'].initial = date.today()
            self.fields['expected_delivery_date'].initial = date.today() + timedelta(days=7)
        
        # Add empty labels for required dropdowns
        self.fields['supplier'].empty_label = "Select Supplier"
        self.fields['transporter'].empty_label = "Select Transporter (Optional)"
        
        # Add required field indicators
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
    
    def clean_expected_delivery_date(self):
        """Validate expected delivery date"""
        expected_date = self.cleaned_data.get('expected_delivery_date')
        po_date = self.cleaned_data.get('po_date')
        
        if expected_date and po_date:
            if expected_date < po_date:
                raise ValidationError(
                    "Expected delivery date cannot be before PO date."
                )
            
            # Warn if delivery date is too far in future (more than 90 days)
            if (expected_date - po_date).days > 90:
                raise ValidationError(
                    "Expected delivery date is more than 90 days from PO date. Please verify."
                )
        
        return expected_date
    
    def clean_discount_percentage(self):
        """Validate discount percentage"""
        discount = self.cleaned_data.get('discount_percentage')
        if discount and (discount < 0 or discount > 100):
            raise ValidationError(
                "Discount percentage must be between 0 and 100."
            )
        return discount
    
    def clean(self):
        """Additional form validation"""
        cleaned_data = super().clean()
        print(f"=== FORM CLEAN DEBUG ===")
        print(f"Cleaned data: {cleaned_data}")
        print(f"Form errors: {self.errors}")
        print(f"=== END FORM CLEAN ===")
        return cleaned_data


class PurchaseOrderItemForm(forms.ModelForm):
    """
    Form for individual Purchase Order Items
    """
    
    class Meta:
        model = PurchaseOrderItem
        fields = [
            'item', 'quantity', 'unit_rate', 'tax_rate', 
            'notes', 'expected_delivery_date'
        ]
        
        widgets = {
            'item': forms.Select(attrs={
                'class': 'form-select item-select',
                'onchange': 'loadItemDetails(this)'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input',
                'step': '0.01',
                'min': '0.01',
                'onchange': 'calculateLineTotal(this)'
            }),
            'unit_rate': forms.NumberInput(attrs={
                'class': 'form-control rate-input',
                'step': '0.01',
                'min': '0.01',
                'onchange': 'calculateLineTotal(this)'
            }),
            'tax_rate': forms.NumberInput(attrs={
                'class': 'form-control tax-rate-input',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'onchange': 'calculateLineTotal(this)'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item-specific notes (optional)'
            }),
            'expected_delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter active items
        self.fields['item'].queryset = Item.objects.filter(
            status='active'
        ).order_by('item_name')
        
        # Set required fields
        self.fields['item'].required = True
        self.fields['quantity'].required = True
        self.fields['unit_rate'].required = True
        
        # Add empty label
        self.fields['item'].empty_label = "Select Item"
        
        # Set initial tax rate from item if creating new
        if not self.instance.pk and self.instance.item_id:
            item = Item.objects.get(pk=self.instance.item_id)
            self.fields['tax_rate'].initial = item.tax_rate
    
    def clean_quantity(self):
        """Validate quantity"""
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        return quantity
    
    def clean_unit_rate(self):
        """Validate unit rate"""
        rate = self.cleaned_data.get('unit_rate')
        if rate and rate <= 0:
            raise ValidationError("Unit rate must be greater than 0.")
        return rate


# Create formset for PO Items
PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True,
    fields=['item', 'quantity', 'unit_rate', 'tax_rate', 'notes', 'expected_delivery_date']
)


class PurchaseOrderSearchForm(forms.Form):
    """
    Form for searching and filtering Purchase Orders
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by PO number, supplier, or reference...',
            'autofocus': True
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + list(PurchaseOrderStatus.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    priority = forms.ChoiceField(
        required=False,
        choices=[('', 'All Priorities')] + list(PurchaseOrderPriority.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    supplier = forms.ModelChoiceField(
        required=False,
        queryset=Supplier.objects.filter(status='active').order_by('supplier_name'),
        empty_label="All Suppliers",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
