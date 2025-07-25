# items/models.py
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils import timezone

class ItemCategory(models.TextChoices):
    RAW_MATERIAL = 'raw_material', 'Raw Material'
    PACKAGING = 'packaging', 'Packaging'
    STATIONERY = 'stationery', 'Stationery' 
    INFRASTRUCTURE = 'infrastructure', 'Infrastructure'
    OTHERS = 'others', 'Others'

class ItemClassification(models.TextChoices):
    A = 'A', 'A - High Value/High Usage'
    B = 'B', 'B - Medium Value/Medium Usage'
    C = 'C', 'C - Low Value/Low Usage'

class ItemStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    DISCONTINUED = 'discontinued', 'Discontinued'

class Item(models.Model):
    """
    Enhanced Item Master model for Mithila Foods
    Includes MVP features for comprehensive item management
    """
    # Basic Item Information
    item_id = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False,
        help_text="Auto-generated Item ID"
    )
    item_name = models.CharField(
        max_length=200,
        help_text="Name of the item"
    )
    category = models.CharField(
        max_length=20,
        choices=ItemCategory.choices,
        default=ItemCategory.OTHERS,
        help_text="Item category classification"
    )
    
    # Enhanced Fields (MVP additions)
    hsn_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="HSN/SAC Code for GST compliance"
    )
    unit = models.CharField(
        max_length=20,
        help_text="Unit of measurement (kg, pcs, rolls, liters, etc.)"
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00,
        validators=[MinValueValidator(0)],
        help_text="GST rate percentage"
    )
    
    # Inventory Management Fields (simplified)
    reorder_level = models.PositiveIntegerField(
        default=0,
        help_text="Minimum stock level for reordering"
    )
    # maximum_stock field removed as per request
    standard_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Standard/benchmark rate without GST"
    )
    
    # Business Classification (removed as per request)
    # classification field removed
    # lead_time_days field removed
    
    # Quality & Compliance
    shelf_life_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Shelf life in days (for perishable items)"
    )
    specification = models.TextField(
        blank=True,
        help_text="Item specifications and quality parameters"
    )
    
    # Status and Tracking
    status = models.CharField(
        max_length=15,
        choices=ItemStatus.choices,
        default=ItemStatus.ACTIVE
    )
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(
        max_length=100,
        blank=True,
        help_text="User who created this item"
    )
    updated_by = models.CharField(
        max_length=100,
        blank=True,
        help_text="User who last updated this item"
    )
    
    # Additional Information
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the item"
    )
    remarks = models.TextField(
        blank=True,
        help_text="Additional remarks or notes"
    )
    
    class Meta:
        db_table = 'item_master'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['item_name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['item_name']),
        ]

    def __str__(self):
        return f"{self.item_id} - {self.item_name}"
    
    def save(self, *args, **kwargs):
        """Auto-generate item ID if not provided"""
        if not self.item_id:
            # Get the last item ID and increment
            last_item = Item.objects.filter(
                item_id__startswith='ITM'
            ).order_by('-id').first()
            
            if last_item:
                try:
                    last_number = int(last_item.item_id.split('-')[1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
                
            self.item_id = f"ITM-{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('items:item_detail', kwargs={'pk': self.pk})
    
    @property
    def is_active(self):
        return self.status == ItemStatus.ACTIVE
    
    @property
    def needs_reorder(self):
        """Check if item needs reordering (placeholder for inventory integration)"""
        # This would integrate with inventory management in future
        return False
    
    @property
    def category_display(self):
        return self.get_category_display()

# Optional: Item Supplier Mapping (for future integration)
class ItemSupplier(models.Model):
    """
    Maps items to preferred suppliers with ratings
    This will integrate with Supplier Master in future phases
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_suppliers')
    supplier_name = models.CharField(max_length=200)  # Temporary field until Supplier model is created
    preference_order = models.PositiveIntegerField(default=1, help_text="1 = Most preferred")
    last_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Last quoted rate from this supplier"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'item_supplier_mapping'
        unique_together = ['item', 'supplier_name']
        ordering = ['preference_order']
    
    def __str__(self):
        return f"{self.item.item_name} - {self.supplier_name}"
