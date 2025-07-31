# suppliers/models.py
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone

class SupplierCategory(models.TextChoices):
    """Categories for suppliers based on business type"""
    MANUFACTURER = 'manufacturer', 'Manufacturer'
    DISTRIBUTOR = 'distributor', 'Distributor'  
    WHOLESALER = 'wholesaler', 'Wholesaler'
    RETAILER = 'retailer', 'Retailer'
    SERVICE_PROVIDER = 'service_provider', 'Service Provider'
    RAW_MATERIAL = 'raw_material', 'Raw Material Supplier'
    PACKAGING = 'packaging', 'Packaging Supplier'
    OTHERS = 'others', 'Others'

class SupplierStatus(models.TextChoices):
    """Status choices for suppliers"""
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    BLACKLISTED = 'blacklisted', 'Blacklisted'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    SUSPENDED = 'suspended', 'Suspended'

class PaymentTerms(models.TextChoices):
    """Payment terms for suppliers"""
    IMMEDIATE = 'immediate', 'Immediate'
    NET_7 = 'net_7', 'Net 7 Days'
    NET_15 = 'net_15', 'Net 15 Days'
    NET_30 = 'net_30', 'Net 30 Days'
    NET_45 = 'net_45', 'Net 45 Days'
    NET_60 = 'net_60', 'Net 60 Days'
    ADVANCE = 'advance', 'Advance Payment'
    COD = 'cod', 'Cash on Delivery'

class SupplierRating(models.TextChoices):
    """Supplier performance rating"""
    EXCELLENT = 'excellent', 'Excellent (A+)'
    GOOD = 'good', 'Good (A)'
    AVERAGE = 'average', 'Average (B)'
    BELOW_AVERAGE = 'below_average', 'Below Average (C)'
    POOR = 'poor', 'Poor (D)'
    NOT_RATED = 'not_rated', 'Not Rated'

class Supplier(models.Model):
    """
    Enhanced Supplier model with all requested features
    (No items/transporters selection - simplified version)
    """
    
    # Primary Information
    supplier_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated unique supplier ID"
    )
    
    supplier_name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Official supplier/company name"
    )
    
    contact_person = models.CharField(
        max_length=100,
        help_text="Primary contact person name"
    )
    
    category = models.CharField(
        max_length=20,
        choices=SupplierCategory.choices,
        default=SupplierCategory.MANUFACTURER,
        help_text="Supplier business category"
    )
    
    status = models.CharField(
        max_length=20,
        choices=SupplierStatus.choices,
        default=SupplierStatus.PENDING_APPROVAL,
        help_text="Current supplier status"
    )
    
    # Contact Information
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = models.CharField(
        validators=[phone_validator],
        max_length=17,
        help_text="Primary phone number"
    )
    
    alternate_phone = models.CharField(
        validators=[phone_validator],
        max_length=17,
        blank=True,
        null=True,
        help_text="Alternative phone number"
    )
    
    # ENHANCED FEATURE: Email (OPTIONAL)
    email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True,
        help_text="Primary email address (OPTIONAL)"
    )
    
    alternate_email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True,
        help_text="Alternative email address"
    )
    
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Company website URL"
    )
    
    # Address Information
    address_line_1 = models.CharField(
        max_length=200,
        help_text="Street address line 1"
    )
    
    address_line_2 = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Street address line 2 (optional)"
    )
    
    city = models.CharField(
        max_length=100,
        help_text="City"
    )
    
    state = models.CharField(
        max_length=100,
        help_text="State/Province"
    )
    
    postal_code = models.CharField(
        max_length=20,
        help_text="Postal/ZIP code"
    )
    
    country = models.CharField(
        max_length=100,
        default='India',
        help_text="Country"
    )
    
    # Business Information
    gstin = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="GST Identification Number (15 digits)",
        validators=[RegexValidator(
            regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
            message="Enter a valid GSTIN (15 characters)"
        )]
    )
    
    pan_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="PAN Card Number",
        validators=[RegexValidator(
            regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
            message="Enter a valid PAN number (e.g., ABCDE1234F)"
        )]
    )
    
    # Financial Information
    payment_terms = models.CharField(
        max_length=20,
        choices=PaymentTerms.choices,
        default=PaymentTerms.NET_30,
        help_text="Default payment terms"
    )
    
    # ENHANCED FEATURE: Credit Limit (OPTIONAL)
    credit_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Credit limit amount (OPTIONAL)"
    )
    
    # Performance Metrics
    rating = models.CharField(
        max_length=20,
        choices=SupplierRating.choices,
        default=SupplierRating.NOT_RATED,
        help_text="Supplier performance rating"
    )
    
    # ENHANCED FEATURE: Bank Information (OPTIONAL)
    bank_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Bank name (OPTIONAL)"
    )
    
    account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Bank account number (OPTIONAL)"
    )
    
    ifsc_code = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        help_text="IFSC code (OPTIONAL)",
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',
            message="Enter a valid IFSC code (e.g., SBIN0001234)"
        )]
    )
    
    # ENHANCED FEATURE: UPI Information (OPTIONAL)
    upi_scanner_image = models.ImageField(
        upload_to='upi_scanners/',
        blank=True,
        null=True,
        help_text="UPI QR code scanner image (OPTIONAL)"
    )
    
    # Additional Information
    products_services = models.TextField(
        blank=True,
        null=True,
        help_text="Products/services offered by supplier"
    )
    
    # PHASE 1 ENHANCEMENT: Many-to-Many Relationships
    items_supplied = models.ManyToManyField(
        'items.Item',
        blank=True,
        related_name='suppliers',
        help_text="Items that this supplier can provide"
    )
    
    preferred_transporters = models.ManyToManyField(
        'transporters.Transporter',
        blank=True,
        related_name='preferred_by_suppliers',
        help_text="Preferred transporters for this supplier"
    )
    
    remarks = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or comments"
    )
    
    # Audit Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(
        max_length=100,
        default='System',
        help_text="User who created this supplier"
    )
    
    class Meta:
        db_table = 'supplier_master'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['supplier_name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['supplier_name']),
            models.Index(fields=['gstin']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.supplier_id:
            # Generate supplier ID: SUP + YYYYMM + sequential number
            from django.db.models import Max
            current_month = timezone.now().strftime('%Y%m')
            last_supplier = Supplier.objects.filter(
                supplier_id__startswith=f'SUP{current_month}'
            ).aggregate(Max('supplier_id'))
            
            if last_supplier['supplier_id__max']:
                last_number = int(last_supplier['supplier_id__max'][-4:])
                next_number = last_number + 1
            else:
                next_number = 1
            
            self.supplier_id = f'SUP{current_month}{next_number:04d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.supplier_id} - {self.supplier_name}"
    
    def get_absolute_url(self):
        return reverse('suppliers:supplier_detail', kwargs={'pk': self.pk})
    
    @property
    def full_address(self):
        """Return complete formatted address"""
        address_parts = [self.address_line_1]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        address_parts.extend([self.city, self.state, self.postal_code, self.country])
        return ', '.join(address_parts)
    
    @property
    def category_display(self):
        return self.get_category_display()
    
    @property
    def status_display(self):
        return self.get_status_display()
    
    @property
    def rating_display(self):
        return self.get_rating_display()
    
    @property
    def is_active(self):
        return self.status == SupplierStatus.ACTIVE
    
    @property
    def days_since_created(self):
        return (timezone.now() - self.created_at).days
    
    @property
    def has_bank_details(self):
        """Check if supplier has bank information"""
        return bool(self.bank_name or self.account_number or self.ifsc_code)
    
    @property
    def has_upi_scanner(self):
        """Check if supplier has UPI scanner image"""
        return bool(self.upi_scanner_image)
