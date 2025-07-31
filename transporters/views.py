# transporters/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from .models import (
    Transporter, TransporterStatus, VehicleType, RateType, TransporterRating
)
from .forms import TransporterForm, TransporterSearchForm

# Professional Transporter Views

class TransporterListView(ListView):
    """Professional Transporter List View"""
    model = Transporter
    template_name = 'transporters/transporter_list.html'
    context_object_name = 'transporters'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transporter.objects.all()
        
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        vehicle_type_filter = self.request.GET.get('vehicle_type', '')
        rating_filter = self.request.GET.get('rating', '')
        services_city_filter = self.request.GET.get('services_city', '')
        carries_item_filter = self.request.GET.get('carries_item', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(transporter_name__icontains=search_query) |
                Q(transporter_id__icontains=search_query) |
                Q(contact_person__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(custom_locations__icontains=search_query)
            )
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if vehicle_type_filter:
            queryset = queryset.filter(primary_vehicle_type=vehicle_type_filter)
        if rating_filter:
            queryset = queryset.filter(rating=rating_filter)
        
        # Enhanced filtering
        if services_city_filter:
            queryset = queryset.filter(serviceable_cities__id=services_city_filter)
        if carries_item_filter:
            queryset = queryset.filter(items_carried__id=carries_item_filter)
        
        return queryset.distinct().order_by('transporter_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TransporterSearchForm(self.request.GET)
        context['title'] = 'Transporter Management'
        context['total_transporters'] = Transporter.objects.count()
        context['active_transporters'] = Transporter.objects.filter(status='active').count()
        return context

class TransporterDetailView(DetailView):
    """Professional Transporter Detail View"""
    model = Transporter
    template_name = 'transporters/transporter_detail.html'
    context_object_name = 'transporter'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transporter = self.get_object()
        
        # Additional context
        context['title'] = f'Transporter Details - {transporter.transporter_name}'
        
        return context

class TransporterCreateView(CreateView):
    """Professional Transporter Create View"""
    model = Transporter
    form_class = TransporterForm
    template_name = 'transporters/transporter_form.html'
    success_url = reverse_lazy('transporters:transporter_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Transporter'
        context['form_action'] = 'Create'
        return context
    
    def form_valid(self, form):
        form.instance.created_by = getattr(self.request.user, 'username', 'System')
        
        # Save the instance first
        response = super().form_valid(form)
        
        # Now get the saved instance with ManyToMany relationships
        transporter = form.instance
        
        # Success message
        success_msg = f'✅ Transporter "{transporter.transporter_name}" created successfully!'
        
        # Add service locations to success message
        locations = transporter.locations_list
        if locations:
            if len(locations) > 3:
                locations_display = ', '.join(locations[:3]) + f' and {len(locations)-3} more'
            else:
                locations_display = ', '.join(locations)
            success_msg += f' Services: {locations_display}.'
        
        # Add payment details to success message
        if transporter.has_payment_details:
            success_msg += f' Payment details added.'
        if transporter.has_upi_scanner:
            success_msg += f' UPI scanner uploaded.'
            
        messages.success(self.request, success_msg)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Please correct the errors below.')
        return super().form_invalid(form)

class TransporterUpdateView(UpdateView):
    """Professional Transporter Update View"""
    model = Transporter
    form_class = TransporterForm
    template_name = 'transporters/transporter_form.html'
    success_url = reverse_lazy('transporters:transporter_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Transporter - {self.get_object().transporter_name}'
        context['form_action'] = 'Update'
        return context
    
    def form_valid(self, form):
        # Save the instance first
        response = super().form_valid(form)
        
        # Now get the saved instance with ManyToMany relationships
        transporter = form.instance
        
        # Success message
        success_msg = f'✅ Transporter "{transporter.transporter_name}" updated successfully!'
        
        # Add service locations to success message
        locations = transporter.locations_list
        if locations:
            if len(locations) > 3:
                locations_display = ', '.join(locations[:3]) + f' and {len(locations)-3} more'
            else:
                locations_display = ', '.join(locations)
            success_msg += f' Services: {locations_display}.'
        
        # Add payment details to success message
        if transporter.has_payment_details:
            success_msg += f' Payment details updated.'
        if transporter.has_upi_scanner:
            success_msg += f' UPI scanner updated.'
            
        messages.success(self.request, success_msg)
        return response

class TransporterDeleteView(DeleteView):
    """Professional Transporter Delete View"""
    model = Transporter
    template_name = 'transporters/transporter_confirm_delete.html'
    success_url = reverse_lazy('transporters:transporter_list')
    
    def delete(self, request, *args, **kwargs):
        transporter = self.get_object()
        messages.success(
            request, 
            f'✅ Transporter "{transporter.transporter_name}" deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)

# Professional Dashboard View
def transporters_dashboard(request):
    """Professional Transporter Dashboard with Statistics"""
    
    # Basic statistics
    total_transporters = Transporter.objects.count()
    active_transporters = Transporter.objects.filter(status='active').count()
    pending_transporters = Transporter.objects.filter(status='pending_approval').count()
    
    # Vehicle type breakdown
    vehicle_stats = {}
    for vehicle_code, vehicle_name in VehicleType.choices:
        count = Transporter.objects.filter(primary_vehicle_type=vehicle_code).count()
        vehicle_stats[vehicle_name] = count
    
    # Rating breakdown
    rating_stats = {}
    for rating_code, rating_name in TransporterRating.choices:
        count = Transporter.objects.filter(rating=rating_code).count()
        rating_stats[rating_name] = count
    
    # Fleet statistics (using database aggregation to handle NULL values properly)
    total_fleet_size = Transporter.objects.aggregate(
        total_fleet=Sum('fleet_size')
    )['total_fleet'] or 0
    transporters_with_business_details = Transporter.objects.filter(
        Q(gstin__isnull=False) | Q(pan_number__isnull=False) | 
        Q(license_number__isnull=False) | Q(registration_number__isnull=False)
    ).count()
    transporters_with_payment_details = Transporter.objects.filter(
        Q(bank_name__isnull=False) | Q(account_number__isnull=False) | Q(ifsc_code__isnull=False)
    ).count()
    transporters_with_upi = Transporter.objects.exclude(upi_scanner_image='').count()
    
    # Recent transporters
    recent_transporters = Transporter.objects.order_by('-created_at')[:5]
    
    context = {
        'title': 'Transporter Dashboard',
        'total_transporters': total_transporters,
        'active_transporters': active_transporters,
        'pending_transporters': pending_transporters,
        'vehicle_stats': vehicle_stats,
        'rating_stats': rating_stats,
        'total_fleet_size': total_fleet_size,
        'transporters_with_business_details': transporters_with_business_details,
        'transporters_with_payment_details': transporters_with_payment_details,
        'transporters_with_upi': transporters_with_upi,
        'recent_transporters': recent_transporters,
        'compulsory_fields': [
            'Transporter ID (Auto-generated)',
            'Transporter Name',
            'Address',
            'Phone Number',
            'Locations Serviceable'
        ]
    }
    
    return render(request, 'transporters/dashboard.html', context)

# AJAX Views for dynamic functionality
def transporter_quick_search(request):
    """Quick search for transporters"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'transporters': []})
    
    transporters = Transporter.objects.filter(
        Q(transporter_name__icontains=query) |
        Q(transporter_id__icontains=query) |
        Q(contact_person__icontains=query) |
        Q(serviceable_locations__icontains=query)
    )[:10]
    
    data = {
        'transporters': [
            {
                'id': transporter.id,
                'transporter_id': transporter.transporter_id,
                'name': transporter.transporter_name,
                'contact_person': transporter.contact_person,
                'status': transporter.get_status_display(),
                'vehicle_type': transporter.get_primary_vehicle_type_display(),
                'fleet_size': transporter.fleet_size,
                'locations': transporter.locations_list[:3]  # First 3 locations
            }
            for transporter in transporters
        ]
    }
    
    return JsonResponse(data)

# API endpoint for transporter statistics
def transporter_stats_api(request):
    """API endpoint for dashboard statistics"""
    total_fleet = Transporter.objects.aggregate(
        total_fleet=Sum('fleet_size')
    )['total_fleet'] or 0
    
    stats = {
        'total': Transporter.objects.count(),
        'active': Transporter.objects.filter(status='active').count(),
        'pending': Transporter.objects.filter(status='pending_approval').count(),
        'total_fleet': total_fleet,
        'with_business_details': Transporter.objects.filter(
            Q(gstin__isnull=False) | Q(pan_number__isnull=False)
        ).count(),
    }
    
    return JsonResponse(stats)
