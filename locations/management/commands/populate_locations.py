# locations/management/commands/populate_locations.py
from django.core.management.base import BaseCommand
from locations.models import State, District

class Command(BaseCommand):
    help = 'Populate Indian states and major districts'

    def handle(self, *args, **options):
        # Sample Indian states and districts
        states_data = {
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik', 'Aurangabad', 'Solapur', 'Kolhapur'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Jamnagar', 'Gandhinagar'],
            'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum', 'Gulbarga', 'Bellary'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli', 'Tirunelveli'],
            'Delhi': ['New Delhi', 'North Delhi', 'South Delhi', 'East Delhi', 'West Delhi', 'Central Delhi'],
            'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Bikaner', 'Ajmer', 'Bhilwara'],
            'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Ghaziabad', 'Agra', 'Varanasi', 'Meerut', 'Allahabad'],
            'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri', 'Malda', 'Bardhaman'],
            'Haryana': ['Gurgaon', 'Faridabad', 'Panipat', 'Ambala', 'Yamunanagar', 'Rohtak'],
            'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda', 'Hoshiarpur'],
        }

        self.stdout.write(self.style.SUCCESS('Creating states and districts...'))

        for state_name, districts in states_data.items():
            # Create or get state
            state, created = State.objects.get_or_create(
                name=state_name,
                defaults={'code': state_name[:3].upper()}
            )
            
            if created:
                self.stdout.write(f'Created state: {state_name}')
            
            # Create districts
            for district_name in districts:
                district, created = District.objects.get_or_create(
                    name=district_name,
                    state=state
                )
                
                if created:
                    self.stdout.write(f'  Created district: {district_name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {State.objects.count()} states and {District.objects.count()} districts'
            )
        )
