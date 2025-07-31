# purchase_orders/models.py
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from items.models import Item
from suppliers.models import Supplier
from transporters.models import Transporter


class PurchaseOrderStatus(models.TextChoices):
    """Status choices for purchase orders"""
    DRAFT = 'draft', 'Draft'
    PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
    APPROVED = 'approved', 'Approved'
    SENT_TO_SUPPLIER = 'sent_to_supplier', 'Sent to Supplier'
    CONFIRMED = 'confirmed', 'Confirmed by Supplier'
    IN_TRANSIT = 'in_transit', 'In Transit'
    PARTIALLY_DELIVERED = 'partially_delivered', 'Partially Delivered'
    DELIVERED = 'delivered', 'Delivered'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    ON_HOLD = 'on_hold', 'On Hold'


class PurchaseOrderPriority(models.TextChoices):
    """Priority levels for purchase orders"""
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


class PaymentTerms(models.TextChoices):
    """Payment terms for purchase orders"""
    IMMEDIATE = 'immediate', 'Immediate Payment'
    NET_7 = 'net_7', 'Net 7 Days'
    NET_15 = 'net_15', 'Net 15 Days'
    NET_30 = 'net_30', 'Net 30 Days'
    NET_45 = 'net_45', 'Net 45 Days'
    NET_60 = 'net_60', 'Net 60 Days'
    ADVANCE_50 = 'advance_50', '50% Advance'
    ADVANCE_100 = 'advance_100', '100% Advance'
    COD = 'cod', 'Cash on Delivery'


class PurchaseOrder(models.Model):
    """
    Enhanced Purchase Order model for Mithila Foods
    Integrates with Items, Suppliers, and Transporters
    """
    
    # Primary Information
    po_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated PO number"
    )
    
    # Related Models
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='purchase_orders',
        help_text="Supplier for this purchase order"
    )
    
    transporter = models.ForeignKey(
        Transporter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_orders',
        help_text="Assigned transporter (optional)"
    )
    
    # Order Information
    po_date = models.DateField(
        default=timezone.now,
        help_text="Purchase order date"
    )
    
    expected_delivery_date = models.DateField(
        help_text="Expected delivery date"
    )
    
    actual_delivery_date = models.DateField(
        null=True,
        blank=True,
        help_text="Actual delivery date"
    )
    
    # Status and Priority
    status = models.CharField(
        max_length=20,
        choices=PurchaseOrderStatus.choices,
        default=PurchaseOrderStatus.DRAFT,
        help_text="Current status of the purchase order"
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PurchaseOrderPriority.choices,
        default=PurchaseOrderPriority.NORMAL,
        help_text="Priority level"
    )
    
    # Financial Information
    payment_terms = models.CharField(
        max_length=20,
        choices=PaymentTerms.choices,
        default=PaymentTerms.NET_30,
        help_text="Payment terms"
    )
    
    subtotal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Subtotal before tax"
    )
    
    tax_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total tax amount"
    )
    
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total amount including tax"
    )
    
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        help_text="Discount percentage"
    )
    
    discount_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Discount amount"
    )
    
    # Delivery Information
    delivery_address = models.TextField(
        help_text="Delivery address"
    )
    
    delivery_contact_person = models.CharField(
        max_length=100,
        help_text="Contact person for delivery"
    )
    
    delivery_phone = models.CharField(
        max_length=17,
        help_text="Delivery contact phone"
    )
    
    # Additional Information
    reference_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="External reference number"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or instructions"
    )
    
    terms_and_conditions = models.TextField(
        blank=True,
        null=True,
        help_text="Terms and conditions"
    )
    
    # Approval Information
    approved_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Approved by user"
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Approval timestamp"
    )
    
    # Audit Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(
        max_length=100,
        default='System',
        help_text="User who created this PO"
    )
    updated_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="User who last updated this PO"
    )
    
    class Meta:
        db_table = 'purchase_order'
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['po_date']),
            models.Index(fields=['supplier']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        """Auto-generate PO number if not provided"""
        if not self.po_number:
            # Generate PO number: PO + YYYYMM + sequential number
            from django.db.models import Max
            current_month = timezone.now().strftime('%Y%m')
            last_po = PurchaseOrder.objects.filter(
                po_number__startswith=f'PO{current_month}'
            ).aggregate(Max('po_number'))
            
            if last_po['po_number__max']:
                last_number = int(last_po['po_number__max'][-4:])
                next_number = last_number + 1
            else:
                next_number = 1
            
            self.po_number = f'PO{current_month}{next_number:04d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.supplier_name}"
    
    def get_absolute_url(self):
        return reverse('purchase_orders:po_detail', kwargs={'pk': self.pk})
    
    @property
    def is_editable(self):
        """Check if PO can be edited"""
        return self.status in [PurchaseOrderStatus.DRAFT, PurchaseOrderStatus.PENDING_APPROVAL]
    
    @property
    def is_approved(self):
        """Check if PO is approved"""
        return self.status not in [PurchaseOrderStatus.DRAFT, PurchaseOrderStatus.PENDING_APPROVAL, PurchaseOrderStatus.CANCELLED]
    
    @property
    def days_since_created(self):
        """Days since PO was created"""
        return (timezone.now() - self.created_at).days
    
    @property
    def is_overdue(self):
        """Check if delivery is overdue"""
        if self.status in [PurchaseOrderStatus.DELIVERED, PurchaseOrderStatus.COMPLETED]:
            return False
        return timezone.now().date() > self.expected_delivery_date
    
    @property
    def status_color(self):
        """Get status color for UI"""
        status_colors = {
            PurchaseOrderStatus.DRAFT: 'secondary',
            PurchaseOrderStatus.PENDING_APPROVAL: 'warning',
            PurchaseOrderStatus.APPROVED: 'info',
            PurchaseOrderStatus.SENT_TO_SUPPLIER: 'primary',
            PurchaseOrderStatus.CONFIRMED: 'success',
            PurchaseOrderStatus.IN_TRANSIT: 'info',
            PurchaseOrderStatus.PARTIALLY_DELIVERED: 'warning',
            PurchaseOrderStatus.DELIVERED: 'success',
            PurchaseOrderStatus.COMPLETED: 'success',
            PurchaseOrderStatus.CANCELLED: 'danger',
            PurchaseOrderStatus.ON_HOLD: 'dark',
        }
        return status_colors.get(self.status, 'secondary')
    
    @property
    def priority_color(self):
        """Get priority color for UI"""
        priority_colors = {
            PurchaseOrderPriority.LOW: 'success',
            PurchaseOrderPriority.NORMAL: 'primary',
            PurchaseOrderPriority.HIGH: 'warning',
            PurchaseOrderPriority.URGENT: 'danger',
        }
        return priority_colors.get(self.priority, 'primary')
    
    def calculate_totals(self):
        """Calculate and update order totals"""
        items = self.items.all()
        
        self.subtotal = sum(item.line_total for item in items)
        self.tax_amount = sum(item.tax_amount for item in items)
        
        # Apply discount
        if self.discount_percentage > 0:
            self.discount_amount = (self.subtotal * self.discount_percentage) / 100
        else:
            self.discount_amount = Decimal('0.00')
        
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        
        self.save(update_fields=['subtotal', 'tax_amount', 'total_amount', 'discount_amount'])


class PurchaseOrderItem(models.Model):
    """
    Purchase Order Line Items
    Links PO with Items and manages quantities, rates, etc.
    """
    
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Related purchase order"
    )
    
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name='purchase_order_items',
        help_text="Item being ordered"
    )
    
    # Quantity and Rate Information
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Quantity to order"
    )
    
    unit_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Rate per unit"
    )
    
    line_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Line total before tax"
    )
    
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Tax rate percentage"
    )
    
    tax_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Tax amount for this line"
    )
    
    line_total_with_tax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Line total including tax"
    )
    
    # Delivery Information
    received_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Quantity received"
    )
    
    pending_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Quantity pending delivery"
    )
    
    # Additional Information
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Item-specific notes"
    )
    
    expected_delivery_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected delivery date for this item"
    )
    
    actual_delivery_date = models.DateField(
        null=True,
        blank=True,
        help_text="Actual delivery date"
    )
    
    class Meta:
        db_table = 'purchase_order_item'
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'
        unique_together = ['purchase_order', 'item']
        ordering = ['id']
    
    def save(self, *args, **kwargs):
        """Calculate line totals and tax"""
        # Calculate line total
        self.line_total = self.quantity * self.unit_rate
        
        # Use item's tax rate if not specified
        if self.tax_rate == 0 and self.item.tax_rate:
            self.tax_rate = self.item.tax_rate
        
        # Calculate tax amount
        self.tax_amount = (self.line_total * self.tax_rate) / 100
        
        # Calculate line total with tax
        self.line_total_with_tax = self.line_total + self.tax_amount
        
        # Calculate pending quantity
        self.pending_quantity = self.quantity - self.received_quantity
        
        super().save(*args, **kwargs)
        
        # Update PO totals
        self.purchase_order.calculate_totals()
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.item.item_name}"
    
    @property
    def is_fully_delivered(self):
        """Check if item is fully delivered"""
        return self.received_quantity >= self.quantity
    
    @property
    def delivery_percentage(self):
        """Calculate delivery percentage"""
        if self.quantity == 0:
            return 0
        return min(100, (self.received_quantity / self.quantity) * 100)


class PurchaseOrderStatusHistory(models.Model):
    """
    Track status changes for purchase orders
    Provides audit trail and timeline
    """
    
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='status_history',
        help_text="Related purchase order"
    )
    
    status = models.CharField(
        max_length=20,
        choices=PurchaseOrderStatus.choices,
        help_text="Status at this point"
    )
    
    changed_at = models.DateTimeField(
        default=timezone.now,
        help_text="When status was changed"
    )
    
    changed_by = models.CharField(
        max_length=100,
        help_text="User who changed the status"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about the status change"
    )
    
    class Meta:
        db_table = 'purchase_order_status_history'
        verbose_name = 'PO Status History'
        verbose_name_plural = 'PO Status History'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.get_status_display()}"


class PurchaseOrderDocument(models.Model):
    """
    Store documents related to purchase orders
    Invoices, delivery notes, etc.
    """
    
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text="Related purchase order"
    )
    
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('po_pdf', 'Purchase Order PDF'),
            ('supplier_quote', 'Supplier Quote'),
            ('invoice', 'Invoice'),
            ('delivery_note', 'Delivery Note'),
            ('payment_receipt', 'Payment Receipt'),
            ('other', 'Other Document'),
        ],
        help_text="Type of document"
    )
    
    document_file = models.FileField(
        upload_to='purchase_orders/documents/%Y/%m/',
        help_text="Document file"
    )
    
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Document description"
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(
        max_length=100,
        default='System',
        help_text="User who uploaded the document"
    )
    
    class Meta:
        db_table = 'purchase_order_document'
        verbose_name = 'PO Document'
        verbose_name_plural = 'PO Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.get_document_type_display()}"
