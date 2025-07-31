# locations/management/commands/populate_cities.py
from django.core.management.base import BaseCommand
from locations.models import State, City

class Command(BaseCommand):
    help = 'Populate top Indian cities for serviceable locations'

    def handle(self, *args, **options):
        # Top 20 Indian cities by business importance
        cities_data = {
            'Maharashtra': [
                ('Mumbai', True), ('Pune', True), ('Nagpur', False), 
                ('Thane', False), ('Nashik', False)
            ],
            'Delhi': [
                ('New Delhi', True), ('Delhi NCR', True)
            ],
            'Karnataka': [
                ('Bangalore', True), ('Mysore', False), ('Hubli', False)
            ],
            'Tamil Nadu': [
                ('Chennai', True), ('Coimbatore', False), ('Madurai', False)
            ],
            'Gujarat': [
                ('Ahmedabad', True), ('Surat', True), ('Vadodara', False), ('Rajkot', False)
            ],
            'West Bengal': [
                ('Kolkata', True), ('Howrah', False)
            ],
            'Rajasthan': [
                ('Jaipur', True), ('Jodhpur', False), ('Udaipur', False)
            ],
            'Uttar Pradesh': [
                ('Lucknow', False), ('Kanpur', False), ('Ghaziabad', False), ('Agra', False)
            ],
            'Haryana': [
                ('Gurgaon', True), ('Faridabad', False), ('Noida', True)
            ],
            'Punjab': [
                ('Ludhiana', False), ('Amritsar', False)
            ],
        }

        self.stdout.write(self.style.SUCCESS('Creating major cities...'))

        for state_name, cities in cities_data.items():
            try:
                state = State.objects.get(name=state_name)
            except State.DoesNotExist:
                # Create state if it doesn't exist
                state = State.objects.create(name=state_name, code=state_name[:3].upper())
                self.stdout.write(f'Created state: {state_name}')
            
            # Create cities
            for city_name, is_major in cities:
                city, created = City.objects.get_or_create(
                    name=city_name,
                    state=state,
                    defaults={'is_major': is_major}
                )
                
                if created:
                    status = "MAJOR" if is_major else "standard"
                    self.stdout.write(f'  Created {status} city: {city_name}')

        # Add "Other/Custom" option
        other_state, _ = State.objects.get_or_create(
            name='Other',
            defaults={'code': 'OTH'}
        )
        
        City.objects.get_or_create(
            name='Custom Location',
            state=other_state,
            defaults={'is_major': False}
        )

        major_cities = City.objects.filter(is_major=True).count()
        total_cities = City.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {total_cities} cities ({major_cities} major cities)'
            )
        )
