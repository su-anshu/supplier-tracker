# transporters/models.py
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone

class TransporterStatus(models.TextChoices):
    """Status choices for transporters"""
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    SUSPENDED = 'suspended', 'Suspended'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    BLACKLISTED = 'blacklisted', 'Blacklisted'

class VehicleType(models.TextChoices):
    """Types of vehicles available"""
    TRUCK = 'truck', 'Truck'
    MINI_TRUCK = 'mini_truck', 'Mini Truck'
    TEMPO = 'tempo', 'Tempo'
    PICKUP = 'pickup', 'Pickup'
    CONTAINER = 'container', 'Container'
    TRAILER = 'trailer', 'Trailer'
    MINI_VAN = 'mini_van', 'Mini Van'
    BIG_VAN = 'big_van', 'Big Van'
    BIKE = 'bike', 'Bike/Motorcycle'
    AUTO_RICKSHAW = 'auto_rickshaw', 'Auto Rickshaw'
    OTHER = 'other', 'Other'

class RateType(models.TextChoices):
    """Rate calculation methods"""
    PER_KM = 'per_km', 'Per Kilometer'
    PER_KG = 'per_kg', 'Per Kilogram'
    FIXED_RATE = 'fixed_rate', 'Fixed Rate'
    PER_TON = 'per_ton', 'Per Ton'
    PER_TRIP = 'per_trip', 'Per Trip'
    NEGOTIABLE = 'negotiable', 'Negotiable'

class TransporterRating(models.TextChoices):
    """Transporter performance rating"""
    EXCELLENT = 'excellent', 'Excellent (A+)'
    GOOD = 'good', 'Good (A)'
    AVERAGE = 'average', 'Average (B)'
    BELOW_AVERAGE = 'below_average', 'Below Average (C)'
    POOR = 'poor', 'Poor (D)'
    NOT_RATED = 'not_rated', 'Not Rated'

class Transporter(models.Model):
    """
    Professional Transporter Master Model
    Manages all transporter information with compulsory and optional fields
    """
    
    # COMPULSORY FIELD 1: Transporter ID (auto-generated)
    transporter_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated unique transporter ID"
    )
    
    # COMPULSORY FIELD 2: Name
    transporter_name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Official transporter/company name"
    )
    
    # Additional Professional Field: Contact Person
    contact_person = models.CharField(
        max_length=100,
        help_text="Primary contact person name"
    )
    
    # Status and Category
    status = models.CharField(
        max_length=20,
        choices=TransporterStatus.choices,
        default=TransporterStatus.PENDING_APPROVAL,
        help_text="Current transporter status"
    )
    
    # COMPULSORY FIELD 4: Phone Number
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
    
    # Optional: Email
    email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True,
        help_text="Primary email address (optional)"
    )
    
    # COMPULSORY FIELD 3: Address
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
    
    # COMPULSORY FIELD 5: Locations Serviceable (enhanced with cities)
    serviceable_locations_text = models.TextField(
        blank=True,
        null=True,
        help_text="Legacy text field for additional location details (optional)"
    )
    
    serviceable_cities = models.ManyToManyField(
        'locations.City',
        blank=True,
        related_name='transporters',
        help_text="Major cities serviceable by this transporter"
    )
    
    custom_locations = models.TextField(
        blank=True,
        null=True,
        help_text="Custom locations not in the standard city list (optional)"
    )
    
    # Additional Professional Fields: Vehicle Information
    primary_vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        blank=True,
        null=True,
        help_text="Primary vehicle type (optional)"
    )
    
    fleet_size = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of vehicles in fleet (optional)"
    )
    
    vehicle_details = models.TextField(
        blank=True,
        null=True,
        help_text="Additional vehicle details, capacity, specifications (optional)"
    )
    
    # Rate Information
    rate_type = models.CharField(
        max_length=20,
        choices=RateType.choices,
        blank=True,
        null=True,
        help_text="Rate calculation method (optional)"
    )
    
    standard_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Standard rate amount (optional)"
    )
    
    # License and Registration
    license_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Transport license number (optional)"
    )
    
    registration_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Business registration number (optional)"
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
    
    # Performance Information
    rating = models.CharField(
        max_length=20,
        choices=TransporterRating.choices,
        default=TransporterRating.NOT_RATED,
        help_text="Transporter performance rating"
    )
    
    # PHASE 1 ENHANCEMENT: Items Carried
    items_carried = models.ManyToManyField(
        'items.Item',
        blank=True,
        related_name='transporters',
        help_text="Types of items this transporter can carry"
    )
    
    # Payment Details (Similar to Suppliers)
    bank_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Bank name (optional)"
    )
    
    account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Bank account number (optional)"
    )
    
    ifsc_code = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        help_text="IFSC code (optional)",
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',
            message="Enter a valid IFSC code (e.g., SBIN0001234)"
        )]
    )
    
    upi_scanner_image = models.ImageField(
        upload_to='transporter_upi_scanners/',
        blank=True,
        null=True,
        help_text="UPI QR code scanner image (optional)"
    )
    
    # Additional Information
    services_offered = models.TextField(
        blank=True,
        null=True,
        help_text="Types of transportation services offered (optional)"
    )
    
    operational_hours = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Operational hours (e.g., 24/7, 9 AM - 6 PM) (optional)"
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
        help_text="User who created this transporter"
    )
    
    class Meta:
        db_table = 'transporter_master'
        verbose_name = 'Transporter'
        verbose_name_plural = 'Transporters'
        ordering = ['transporter_name']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['transporter_name']),
            models.Index(fields=['primary_vehicle_type']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.transporter_id:
            # Generate transporter ID: TR + YYYYMM + sequential number
            from django.db.models import Max
            current_month = timezone.now().strftime('%Y%m')
            last_transporter = Transporter.objects.filter(
                transporter_id__startswith=f'TR{current_month}'
            ).aggregate(Max('transporter_id'))
            
            if last_transporter['transporter_id__max']:
                last_number = int(last_transporter['transporter_id__max'][-4:])
                next_number = last_number + 1
            else:
                next_number = 1
            
            self.transporter_id = f'TR{current_month}{next_number:04d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.transporter_id} - {self.transporter_name}"
    
    def get_absolute_url(self):
        return reverse('transporters:transporter_detail', kwargs={'pk': self.pk})
    
    @property
    def full_address(self):
        """Return complete formatted address"""
        address_parts = [self.address_line_1]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        address_parts.extend([self.city, self.state, self.postal_code, self.country])
        return ', '.join(address_parts)
    
    @property
    def status_display(self):
        return self.get_status_display()
    
    @property
    def vehicle_type_display(self):
        return self.get_primary_vehicle_type_display() if self.primary_vehicle_type else "Not specified"
    
    @property
    def rating_display(self):
        return self.get_rating_display()
    
    @property
    def rate_display(self):
        if self.standard_rate and self.rate_type:
            return f"₹{self.standard_rate} ({self.get_rate_type_display()})"
        elif self.rate_type:
            return self.get_rate_type_display()
        else:
            return "Not specified"
    
    @property
    def fleet_display(self):
        return f"{self.fleet_size} vehicle{'s' if self.fleet_size != 1 else ''}" if self.fleet_size else "Not specified"
    
    @property
    def is_active(self):
        return self.status == TransporterStatus.ACTIVE
    
    @property
    def days_since_created(self):
        return (timezone.now() - self.created_at).days
    
    @property
    def locations_list(self):
        """Return serviceable locations as a list"""
        cities = list(self.serviceable_cities.all().values_list('name', flat=True))
        if self.custom_locations:
            custom_locs = [loc.strip() for loc in self.custom_locations.split(',') if loc.strip()]
            cities.extend(custom_locs)
        return cities
    
    @property
    def has_business_details(self):
        """Check if transporter has business information"""
        return bool(self.gstin or self.pan_number or self.license_number or self.registration_number)
    
    @property
    def has_payment_details(self):
        """Check if transporter has payment information"""
        return bool(self.bank_name or self.account_number or self.ifsc_code)
    
    @property
    def has_upi_scanner(self):
        """Check if transporter has UPI scanner image"""
        return bool(self.upi_scanner_image)
