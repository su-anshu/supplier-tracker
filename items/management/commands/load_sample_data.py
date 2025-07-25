from django.core.management.base import BaseCommand
from items.models import Item, ItemSupplier, ItemCategory, ItemStatus
from django.utils import timezone

class Command(BaseCommand):
    help = 'Load sample data for testing the Item Master module'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample data for Item Master...'))
        
        # Sample items data
        sample_items = [
            {
                'item_name': 'Basmati Rice Premium',
                'category': ItemCategory.RAW_MATERIAL,
                'hsn_code': '1006',
                'unit': 'kg',
                'tax_rate': 5.00,
                'reorder_level': 1000,
                'standard_rate': 85.50,
                'shelf_life_days': 365,
                'specification': 'Premium quality long grain Basmati rice, aged 1 year minimum',
                'description': 'High quality Basmati rice for premium food products'
            },
            {
                'item_name': 'Cardboard Boxes 10x10x5',
                'category': ItemCategory.PACKAGING,
                'hsn_code': '4819',
                'unit': 'pcs',
                'tax_rate': 18.00,
                'reorder_level': 500,
                'standard_rate': 12.50,
                'specification': '3-ply corrugated boxes, food grade',
                'description': 'Standard packaging boxes for 1kg products'
            },
            {
                'item_name': 'Office Paper A4',
                'category': ItemCategory.STATIONERY,
                'hsn_code': '4802',
                'unit': 'ream',
                'tax_rate': 18.00,
                'reorder_level': 50,
                'standard_rate': 285.00,
                'specification': '75 GSM, 500 sheets per ream',
                'description': 'Standard office paper for documentation'
            },
            {
                'item_name': 'Turmeric Powder',
                'category': ItemCategory.RAW_MATERIAL,
                'hsn_code': '0910',
                'unit': 'kg',
                'tax_rate': 5.00,
                'reorder_level': 200,
                'standard_rate': 180.00,
                'shelf_life_days': 730,
                'specification': 'Pure turmeric powder, curcumin content >3%',
                'description': 'High quality turmeric powder for food processing'
            },
            {
                'item_name': 'Plastic Pouches 500g',
                'category': ItemCategory.PACKAGING,
                'hsn_code': '3923',
                'unit': 'pcs',
                'tax_rate': 18.00,
                'reorder_level': 1000,
                'standard_rate': 2.50,
                'specification': 'Food grade laminated pouches with zip lock',
                'description': 'Flexible packaging for spice products'
            },
            {
                'item_name': 'Industrial Weighing Scale',
                'category': ItemCategory.INFRASTRUCTURE,
                'hsn_code': '8423',
                'unit': 'pcs',
                'tax_rate': 18.00,
                'reorder_level': 1,
                'standard_rate': 45000.00,
                'specification': 'Digital scale, 500kg capacity, accuracy ±10g',
                'description': 'Heavy duty weighing scale for production use'
            },
            {
                'item_name': 'Cleaning Detergent',
                'category': ItemCategory.OTHERS,
                'hsn_code': '3402',
                'unit': 'liters',
                'tax_rate': 18.00,
                'reorder_level': 20,
                'standard_rate': 120.00,
                'specification': 'Food grade industrial cleaning detergent',
                'description': 'Cleaning agent for equipment and surfaces'
            },
            {
                'item_name': 'Red Chili Powder',
                'category': ItemCategory.RAW_MATERIAL,
                'hsn_code': '0904',
                'unit': 'kg',
                'tax_rate': 5.00,
                'reorder_level': 150,
                'standard_rate': 220.00,
                'shelf_life_days': 365,
                'specification': 'Kashmiri red chili powder, moisture <10%',
                'description': 'Premium quality red chili powder for spice blends'
            }
        ]
        
        created_count = 0
        
        for item_data in sample_items:
            # Check if item already exists
            if not Item.objects.filter(item_name=item_data['item_name']).exists():
                item_data['created_by'] = 'System'
                item_data['status'] = ItemStatus.ACTIVE
                
                item = Item.objects.create(**item_data)
                created_count += 1
                
                self.stdout.write(f'Created item: {item.item_name} ({item.item_id})')
                
                # Add some sample supplier mappings
                if item.category == ItemCategory.RAW_MATERIAL:
                    suppliers = ['ABC Traders', 'XYZ Supplies', 'Premium Foods Ltd']
                    for i, supplier in enumerate(suppliers[:2]):  # Add 2 suppliers per raw material
                        ItemSupplier.objects.create(
                            item=item,
                            supplier_name=supplier,
                            preference_order=i + 1,
                            last_rate=item.standard_rate * (0.95 + i * 0.1),  # Slightly varied rates
                            is_active=True
                        )
            else:
                self.stdout.write(f'Item already exists: {item_data["item_name"]}')
        
        # Display summary
        total_items = Item.objects.count()
        active_items = Item.objects.filter(status=ItemStatus.ACTIVE).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nSample data loading completed!'))
        self.stdout.write(f'Items created: {created_count}')
        self.stdout.write(f'Total items in database: {total_items}')
        self.stdout.write(f'Active items: {active_items}')
        
        # Show category breakdown
        self.stdout.write('\nCategory breakdown:')
        for category in ItemCategory:
            count = Item.objects.filter(category=category.value).count()
            self.stdout.write(f'  {category.label}: {count} items')
        
        self.stdout.write(self.style.SUCCESS('\nYou can now visit the application to see the sample data!'))
        self.stdout.write('URL: http://localhost:8000/')
