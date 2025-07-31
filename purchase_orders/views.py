# purchase_orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg, F
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import json

from .models import (
    PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus, 
    PurchaseOrderPriority, PurchaseOrderStatusHistory,
    PaymentTerms
)
from items.models import Item
from suppliers.models import Supplier
from transporters.models import Transporter
from .forms import PurchaseOrderForm, PurchaseOrderSearchForm


class PurchaseOrderListView(ListView):
    """
    Enhanced Purchase Order List View with filtering and search
    """
    model = PurchaseOrder
    template_name = 'purchase_orders/po_list.html'
    context_object_name = 'purchase_orders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PurchaseOrder.objects.select_related('supplier', 'transporter').all()
        
        # Get search parameters
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        priority_filter = self.request.GET.get('priority', '')
        supplier_filter = self.request.GET.get('supplier', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        
        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(po_number__icontains=search_query) |
                Q(supplier__supplier_name__icontains=search_query) |
                Q(reference_number__icontains=search_query) |
                Q(delivery_contact_person__icontains=search_query)
            )
        
        # Apply filters
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if supplier_filter:
            queryset = queryset.filter(supplier_id=supplier_filter)
        if date_from:
            queryset = queryset.filter(po_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(po_date__lte=date_to)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add title and search form
        context['title'] = 'Purchase Order Management'
        context['search_form'] = PurchaseOrderSearchForm(self.request.GET)
        
        # Add statistics
        context['total_pos'] = PurchaseOrder.objects.count()
        context['draft_pos'] = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.DRAFT).count()
        context['pending_pos'] = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.PENDING_APPROVAL).count()
        context['approved_pos'] = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.APPROVED).count()
        context['overdue_pos'] = PurchaseOrder.objects.filter(
            expected_delivery_date__lt=timezone.now().date(),
            status__in=[PurchaseOrderStatus.APPROVED, PurchaseOrderStatus.SENT_TO_SUPPLIER, PurchaseOrderStatus.IN_TRANSIT]
        ).count()
        
        # Add total value
        context['total_value'] = PurchaseOrder.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        # Preserve search parameters for pagination
        context['search_params'] = self.request.GET.copy()
        if 'page' in context['search_params']:
            del context['search_params']['page']
        
        return context


class PurchaseOrderDetailView(DetailView):
    """
    Detailed view of a single Purchase Order
    """
    model = PurchaseOrder
    template_name = 'purchase_orders/po_detail.html'
    context_object_name = 'purchase_order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = self.get_object()
        
        # Add related data
        context['po_items'] = po.items.select_related('item').all()
        context['status_history'] = po.status_history.all()[:10]  # Last 10 status changes
        context['documents'] = po.documents.all()
        
        # Add statistics for this PO
        context['total_items'] = po.items.count()
        context['delivered_items'] = po.items.filter(
            received_quantity__gte=F('quantity')
        ).count()
        
        # Calculate delivery progress
        total_qty = po.items.aggregate(total=Sum('quantity'))['total'] or 0
        received_qty = po.items.aggregate(total=Sum('received_quantity'))['total'] or 0
        context['delivery_progress'] = (received_qty / total_qty * 100) if total_qty > 0 else 0
        
        return context


def create_purchase_order(request):
    """
    Simple function-based view to create purchase orders
    """
    if request.method == 'POST':
        try:
            # Create the Purchase Order
            po = PurchaseOrder.objects.create(
                supplier_id=request.POST.get('supplier'),
                transporter_id=request.POST.get('transporter') if request.POST.get('transporter') else None,
                po_date=request.POST.get('po_date'),
                expected_delivery_date=request.POST.get('expected_delivery_date'),
                priority=request.POST.get('priority', 'normal'),
                payment_terms=request.POST.get('payment_terms', 'net_30'),
                delivery_address=request.POST.get('delivery_address'),
                delivery_contact_person=request.POST.get('delivery_contact_person'),
                delivery_phone=request.POST.get('delivery_phone'),
                reference_number=request.POST.get('reference_number', ''),
                discount_percentage=Decimal(request.POST.get('discount_percentage', '0')),
                notes=request.POST.get('notes', ''),
                terms_and_conditions=request.POST.get('terms_and_conditions', ''),
                created_by='System'
            )
            
            # Process items from JSON data
            items_json = request.POST.get('items_data', '[]')
            try:
                items_data = json.loads(items_json)
            except json.JSONDecodeError:
                items_data = []
            
            if not items_data:
                po.delete()
                messages.error(request, '❌ At least one item is required.')
                return redirect('purchase_orders:po_add')
            
            # Create PO Items
            total_items = 0
            for item_data in items_data:
                try:
                    item = Item.objects.get(id=item_data['item_id'])
                    PurchaseOrderItem.objects.create(
                        purchase_order=po,
                        item=item,
                        quantity=Decimal(str(item_data['quantity'])),
                        unit_rate=Decimal(str(item_data['rate'])),
                        tax_rate=Decimal(str(item_data.get('tax_rate', 0)))
                    )
                    total_items += 1
                except (Item.DoesNotExist, KeyError, ValueError) as e:
                    continue
            
            if total_items == 0:
                po.delete()
                messages.error(request, '❌ No valid items could be added.')
                return redirect('purchase_orders:po_add')
            
            # Calculate totals
            po.calculate_totals()
            
            # Create status history
            PurchaseOrderStatusHistory.objects.create(
                purchase_order=po,
                status=po.status,
                changed_by='System',
                notes="Purchase Order created"
            )
            
            messages.success(
                request,
                f'✅ Purchase Order {po.po_number} created successfully with {total_items} items!'
            )
            return redirect('purchase_orders:po_list')
            
        except Exception as e:
            messages.error(request, f'❌ Error creating purchase order: {str(e)}')
            return redirect('purchase_orders:po_add')
    
    # GET request - show form
    context = {
        'title': 'Create New Purchase Order',
        'form': PurchaseOrderForm(),
        'items': Item.objects.filter(status='active').values(
            'id', 'item_name', 'item_id', 'unit', 'standard_rate', 'tax_rate'
        ),
        'suppliers': Supplier.objects.filter(status='active').values(
            'id', 'supplier_name', 'supplier_id'
        ),
        'transporters': Transporter.objects.filter(status='active').values(
            'id', 'transporter_name', 'transporter_id'
        ),
    }
    
    return render(request, 'purchase_orders/po_form_simple.html', context)


# Keep the rest of the views unchanged
class PurchaseOrderUpdateView(UpdateView):
    """
    Update existing Purchase Order
    """
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchase_orders/po_form.html'
    success_url = reverse_lazy('purchase_orders:po_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = self.get_object()
        
        context['title'] = f'Edit Purchase Order - {po.po_number}'
        context['form_action'] = 'Update'
        
        # Check if PO is editable
        if not po.is_editable:
            messages.warning(
                self.request,
                f'⚠️ PO {po.po_number} is in {po.get_status_display()} status and may have limited editing capabilities.'
            )
        
        return context


class PurchaseOrderDeleteView(DeleteView):
    """
    Delete Purchase Order with confirmation
    """
    model = PurchaseOrder
    template_name = 'purchase_orders/po_confirm_delete.html'
    success_url = reverse_lazy('purchase_orders:po_list')
    
    def delete(self, request, *args, **kwargs):
        po = self.get_object()
        
        # Check if PO can be deleted
        if po.status not in [PurchaseOrderStatus.DRAFT, PurchaseOrderStatus.CANCELLED]:
            messages.error(
                request,
                f'❌ Cannot delete PO {po.po_number} with status {po.get_status_display()}'
            )
            return redirect('purchase_orders:po_detail', pk=po.pk)
        
        po_number = po.po_number
        result = super().delete(request, *args, **kwargs)
        
        messages.success(
            request,
            f'✅ Purchase Order {po_number} deleted successfully!'
        )
        return result


# Dashboard view
def purchase_orders_dashboard(request):
    """
    Purchase Orders Dashboard with statistics and analytics
    """
    # Basic statistics
    total_pos = PurchaseOrder.objects.count()
    draft_pos = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.DRAFT).count()
    pending_pos = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.PENDING_APPROVAL).count()
    approved_pos = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.APPROVED).count()
    completed_pos = PurchaseOrder.objects.filter(status=PurchaseOrderStatus.COMPLETED).count()
    
    # Financial statistics
    total_value = PurchaseOrder.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')
    
    avg_po_value = PurchaseOrder.objects.aggregate(
        avg=Avg('total_amount')
    )['avg'] or Decimal('0.00')
    
    # Status breakdown for charts
    status_stats = {}
    for status_code, status_name in PurchaseOrderStatus.choices:
        count = PurchaseOrder.objects.filter(status=status_code).count()
        status_stats[status_name] = count
    
    # Priority breakdown
    priority_stats = {}
    for priority_code, priority_name in PurchaseOrderPriority.choices:
        count = PurchaseOrder.objects.filter(priority=priority_code).count()
        priority_stats[priority_name] = count
    
    # Recent POs
    recent_pos = PurchaseOrder.objects.select_related('supplier').order_by('-created_at')[:10]
    
    # Overdue POs
    overdue_pos = PurchaseOrder.objects.filter(
        expected_delivery_date__lt=timezone.now().date(),
        status__in=[
            PurchaseOrderStatus.APPROVED, 
            PurchaseOrderStatus.SENT_TO_SUPPLIER, 
            PurchaseOrderStatus.IN_TRANSIT
        ]
    ).select_related('supplier')[:5]
    
    # Top suppliers by PO count
    top_suppliers = PurchaseOrder.objects.values(
        'supplier__supplier_name'
    ).annotate(
        po_count=Count('id'),
        total_value=Sum('total_amount')
    ).order_by('-po_count')[:5]
    
    context = {
        'title': 'Purchase Orders Dashboard',
        'total_pos': total_pos,
        'draft_pos': draft_pos,
        'pending_pos': pending_pos,
        'approved_pos': approved_pos,
        'completed_pos': completed_pos,
        'total_value': total_value,
        'avg_po_value': avg_po_value,
        'status_stats': status_stats,
        'priority_stats': priority_stats,
        'recent_pos': recent_pos,
        'overdue_pos': overdue_pos,
        'top_suppliers': top_suppliers,
    }
    
    return render(request, 'purchase_orders/dashboard.html', context)


# AJAX Views and other functions remain the same...
def get_item_details(request):
    """Get item details for AJAX requests"""
    item_id = request.GET.get('item_id')
    if not item_id:
        return JsonResponse({'error': 'No item ID provided'})
    
    try:
        item = Item.objects.get(id=item_id)
        return JsonResponse({
            'item_name': item.item_name,
            'unit': item.unit,
            'standard_rate': float(item.standard_rate) if item.standard_rate else 0,
            'tax_rate': float(item.tax_rate),
            'hsn_code': item.hsn_code or '',
        })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'})


# Function-based views for specific actions
def po_approve(request, pk):
    """Approve a purchase order"""
    po = get_object_or_404(PurchaseOrder, pk=pk)
    
    if po.status != PurchaseOrderStatus.PENDING_APPROVAL:
        messages.error(
            request,
            f'❌ PO {po.po_number} cannot be approved from {po.get_status_display()} status'
        )
        return redirect('purchase_orders:po_detail', pk=pk)
    
    po.status = PurchaseOrderStatus.APPROVED
    po.approved_by = getattr(request.user, 'username', 'System')
    po.approved_at = timezone.now()
    po.save()
    
    # Create status history
    PurchaseOrderStatusHistory.objects.create(
        purchase_order=po,
        status=po.status,
        changed_by=po.approved_by,
        notes="Purchase Order approved"
    )
    
    messages.success(
        request,
        f'✅ Purchase Order {po.po_number} approved successfully!'
    )
    return redirect('purchase_orders:po_detail', pk=pk)


def po_send_to_supplier(request, pk):
    """Send PO to supplier"""
    po = get_object_or_404(PurchaseOrder, pk=pk)
    
    if po.status != PurchaseOrderStatus.APPROVED:
        messages.error(
            request,
            f'❌ PO {po.po_number} must be approved before sending to supplier'
        )
        return redirect('purchase_orders:po_detail', pk=pk)
    
    po.status = PurchaseOrderStatus.SENT_TO_SUPPLIER
    po.save()
    
    # Create status history
    PurchaseOrderStatusHistory.objects.create(
        purchase_order=po,
        status=po.status,
        changed_by=getattr(request.user, 'username', 'System'),
        notes="Purchase Order sent to supplier"
    )
    
    messages.success(
        request,
        f'✅ Purchase Order {po.po_number} sent to supplier!'
    )
    return redirect('purchase_orders:po_detail', pk=pk)


def po_mark_delivered(request, pk):
    """Mark PO as delivered"""
    po = get_object_or_404(PurchaseOrder, pk=pk)
    
    if po.status not in [PurchaseOrderStatus.IN_TRANSIT, PurchaseOrderStatus.PARTIALLY_DELIVERED]:
        messages.error(
            request,
            f'❌ PO {po.po_number} cannot be marked as delivered from {po.get_status_display()} status'
        )
        return redirect('purchase_orders:po_detail', pk=pk)
    
    po.status = PurchaseOrderStatus.DELIVERED
    po.actual_delivery_date = timezone.now().date()
    po.save()
    
    # Create status history
    PurchaseOrderStatusHistory.objects.create(
        purchase_order=po,
        status=po.status,
        changed_by=getattr(request.user, 'username', 'System'),
        notes="Purchase Order marked as delivered"
    )
    
    messages.success(
        request,
        f'✅ Purchase Order {po.po_number} marked as delivered!'
    )
    return redirect('purchase_orders:po_detail', pk=pk)


def get_supplier_details(request):
    """Get supplier details for AJAX requests"""
    supplier_id = request.GET.get('supplier_id')
    if not supplier_id:
        return JsonResponse({'error': 'No supplier ID provided'})
    
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        return JsonResponse({
            'supplier_name': supplier.supplier_name,
            'address': supplier.full_address,
            'phone': supplier.phone_number,
            'email': supplier.email or '',
            'payment_terms': supplier.payment_terms,
        })
    except Supplier.DoesNotExist:
        return JsonResponse({'error': 'Supplier not found'})


def po_quick_search(request):
    """Quick search for POs"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'pos': []})
    
    pos = PurchaseOrder.objects.filter(
        Q(po_number__icontains=query) |
        Q(supplier__supplier_name__icontains=query)
    ).select_related('supplier')[:10]
    
    data = {
        'pos': [
            {
                'id': po.id,
                'po_number': po.po_number,
                'supplier_name': po.supplier.supplier_name,
                'total_amount': float(po.total_amount),
                'status': po.get_status_display(),
                'status_color': po.status_color,
            }
            for po in pos
        ]
    }
    
    return JsonResponse(data)
