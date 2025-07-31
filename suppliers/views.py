# suppliers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from .models import (
    Supplier, SupplierCategory, SupplierStatus, PaymentTerms, SupplierRating
)
from .forms import SupplierForm, SupplierSearchForm

# Enhanced Supplier Views

class SupplierListView(ListView):
    """Enhanced Supplier List View"""
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Supplier.objects.all()
        
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        status_filter = self.request.GET.get('status', '')
        rating_filter = self.request.GET.get('rating', '')
        supplies_item_filter = self.request.GET.get('supplies_item', '')
        has_bank_details_filter = self.request.GET.get('has_bank_details', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(supplier_name__icontains=search_query) |
                Q(supplier_id__icontains=search_query) |
                Q(contact_person__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(city__icontains=search_query)
            )
        
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if rating_filter:
            queryset = queryset.filter(rating=rating_filter)
        
        # Enhanced filtering
        if supplies_item_filter:
            queryset = queryset.filter(items_supplied__id=supplies_item_filter)
        if has_bank_details_filter:
            if has_bank_details_filter == 'yes':
                queryset = queryset.filter(
                    Q(bank_name__isnull=False) & ~Q(bank_name='') &
                    Q(account_number__isnull=False) & ~Q(account_number='')
                )
            elif has_bank_details_filter == 'no':
                queryset = queryset.filter(
                    Q(bank_name__isnull=True) | Q(bank_name='') |
                    Q(account_number__isnull=True) | Q(account_number='')
                )
        
        return queryset.distinct().order_by('supplier_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SupplierSearchForm(self.request.GET)
        context['title'] = 'Supplier Management'
        context['total_suppliers'] = Supplier.objects.count()
        context['active_suppliers'] = Supplier.objects.filter(status='active').count()
        context['inactive_suppliers'] = Supplier.objects.filter(status='inactive').count()
        context['categories_count'] = Supplier.objects.values('category').distinct().count()
        return context

class SupplierDetailView(DetailView):
    """Enhanced Supplier Detail View"""
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.get_object()
        
        # Additional context
        context['title'] = f'Supplier Details - {supplier.supplier_name}'
        
        return context

class SupplierCreateView(CreateView):
    """Enhanced Supplier Create View with ALL FEATURES"""
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Supplier'
        context['form_action'] = 'Create'
        
        # Feature status for template
        context['features_status'] = {
            'email_optional': True,
            'credit_limit_optional': True,
            'bank_details_optional': True,
            'upi_optional': True
        }
        
        return context
    
    def form_valid(self, form):
        form.instance.created_by = getattr(self.request.user, 'username', 'System')
        
        # Enhanced success message
        success_msg = f'✅ Supplier "{form.instance.supplier_name}" created successfully!'
        
        # Add feature details to success message
        if form.instance.email:
            success_msg += f' Email: {form.instance.email}.'
        if form.instance.credit_limit:
            success_msg += f' Credit Limit: ₹{form.instance.credit_limit}.'
        if form.instance.has_bank_details:
            success_msg += f' Bank details added.'
        if form.instance.has_upi_scanner:
            success_msg += f' UPI scanner uploaded.'
            
        messages.success(self.request, success_msg)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Please correct the errors below.')
        return super().form_invalid(form)

class SupplierUpdateView(UpdateView):
    """Enhanced Supplier Update View"""
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Supplier - {self.get_object().supplier_name}'
        context['form_action'] = 'Update'
        
        # Feature status for template
        context['features_status'] = {
            'email_optional': True,
            'credit_limit_optional': True,
            'bank_details_optional': True,
            'upi_optional': True
        }
        
        return context
    
    def form_valid(self, form):
        # Enhanced success message
        success_msg = f'✅ Supplier "{form.instance.supplier_name}" updated successfully!'
        
        # Add feature details to success message
        if form.instance.email:
            success_msg += f' Email: {form.instance.email}.'
        if form.instance.credit_limit:
            success_msg += f' Credit Limit: ₹{form.instance.credit_limit}.'
        if form.instance.has_bank_details:
            success_msg += f' Bank details updated.'
        if form.instance.has_upi_scanner:
            success_msg += f' UPI scanner updated.'
            
        messages.success(self.request, success_msg)
        return super().form_valid(form)

class SupplierDeleteView(DeleteView):
    """Enhanced Supplier Delete View"""
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    
    def delete(self, request, *args, **kwargs):
        supplier = self.get_object()
        messages.success(
            request, 
            f'✅ Supplier "{supplier.supplier_name}" deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)

# Enhanced Dashboard View
def suppliers_dashboard(request):
    """Enhanced Supplier Dashboard with Statistics"""
    
    # Basic statistics
    total_suppliers = Supplier.objects.count()
    active_suppliers = Supplier.objects.filter(status='active').count()
    pending_suppliers = Supplier.objects.filter(status='pending_approval').count()
    
    # Category breakdown
    category_stats = {}
    for category_code, category_name in SupplierCategory.choices:
        count = Supplier.objects.filter(category=category_code).count()
        category_stats[category_name] = count
    
    # Rating breakdown
    rating_stats = {}
    for rating_code, rating_name in SupplierRating.choices:
        count = Supplier.objects.filter(rating=rating_code).count()
        rating_stats[rating_name] = count
    
    # Enhanced features statistics
    suppliers_with_email = Supplier.objects.exclude(email__isnull=True).exclude(email='').count()
    suppliers_with_credit_limit = Supplier.objects.exclude(credit_limit__isnull=True).count()
    suppliers_with_bank_details = Supplier.objects.filter(
        Q(bank_name__isnull=False) | Q(account_number__isnull=False) | Q(ifsc_code__isnull=False)
    ).count()
    suppliers_with_upi = Supplier.objects.exclude(upi_scanner_image='').count()
    
    # Recent suppliers
    recent_suppliers = Supplier.objects.order_by('-created_at')[:5]
    
    context = {
        'title': 'Supplier Dashboard',
        'total_suppliers': total_suppliers,
        'active_suppliers': active_suppliers,
        'pending_suppliers': pending_suppliers,
        'category_stats': category_stats,
        'rating_stats': rating_stats,
        'recent_suppliers': recent_suppliers,
        'enhanced_features_stats': {
            'email_count': suppliers_with_email,
            'credit_limit_count': suppliers_with_credit_limit,
            'bank_details_count': suppliers_with_bank_details,
            'upi_count': suppliers_with_upi,
        },
        'features_implemented': [
            'Email Field (Optional)',
            'Credit Limit (Optional)',
            'Bank Details (Optional)',
            'UPI Scanner Image (Optional)',
            'Professional Forms',
            'Enhanced Dashboard'
        ]
    }
    
    return render(request, 'suppliers/dashboard.html', context)

# AJAX Views for dynamic functionality
def supplier_quick_search(request):
    """Quick search for suppliers"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suppliers': []})
    
    suppliers = Supplier.objects.filter(
        Q(supplier_name__icontains=query) |
        Q(supplier_id__icontains=query) |
        Q(contact_person__icontains=query)
    )[:10]
    
    data = {
        'suppliers': [
            {
                'id': supplier.id,
                'supplier_id': supplier.supplier_id,
                'name': supplier.supplier_name,
                'contact_person': supplier.contact_person,
                'status': supplier.get_status_display(),
                'has_email': bool(supplier.email),
                'has_bank_details': supplier.has_bank_details,
                'has_upi': supplier.has_upi_scanner
            }
            for supplier in suppliers
        ]
    }
    
    return JsonResponse(data)

# API endpoint for supplier statistics
def supplier_stats_api(request):
    """API endpoint for dashboard statistics"""
    stats = {
        'total': Supplier.objects.count(),
        'active': Supplier.objects.filter(status='active').count(),
        'with_email': Supplier.objects.exclude(email__isnull=True).exclude(email='').count(),
        'with_credit_limit': Supplier.objects.exclude(credit_limit__isnull=True).count(),
        'with_bank_details': Supplier.objects.filter(
            Q(bank_name__isnull=False) | Q(account_number__isnull=False) | Q(ifsc_code__isnull=False)
        ).count(),
        'with_upi': Supplier.objects.exclude(upi_scanner_image='').count(),
    }
    
    return JsonResponse(stats)
