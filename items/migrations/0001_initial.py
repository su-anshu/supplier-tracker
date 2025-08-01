# Generated by Django 5.0.1 on 2025-07-22 13:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(editable=False, help_text='Auto-generated Item ID', max_length=20, unique=True)),
                ('item_name', models.CharField(help_text='Name of the item', max_length=200)),
                ('category', models.CharField(choices=[('raw_material', 'Raw Material'), ('packaging', 'Packaging'), ('stationery', 'Stationery'), ('infrastructure', 'Infrastructure'), ('others', 'Others')], default='others', help_text='Item category classification', max_length=20)),
                ('hsn_code', models.CharField(blank=True, help_text='HSN/SAC Code for GST compliance', max_length=10, null=True)),
                ('unit', models.CharField(help_text='Unit of measurement (kg, pcs, rolls, liters, etc.)', max_length=20)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=18.0, help_text='GST rate percentage', max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
                ('reorder_level', models.PositiveIntegerField(default=0, help_text='Minimum stock level for reordering')),
                ('maximum_stock', models.PositiveIntegerField(blank=True, help_text='Maximum stock level', null=True)),
                ('standard_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Standard/benchmark rate without GST', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('classification', models.CharField(choices=[('A', 'A - High Value/High Usage'), ('B', 'B - Medium Value/Medium Usage'), ('C', 'C - Low Value/Low Usage')], default='C', help_text='ABC Classification based on value and usage', max_length=1)),
                ('lead_time_days', models.PositiveIntegerField(default=7, help_text='Standard lead time in days')),
                ('shelf_life_days', models.PositiveIntegerField(blank=True, help_text='Shelf life in days (for perishable items)', null=True)),
                ('specification', models.TextField(blank=True, help_text='Item specifications and quality parameters')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('discontinued', 'Discontinued')], default='active', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, help_text='User who created this item', max_length=100)),
                ('updated_by', models.CharField(blank=True, help_text='User who last updated this item', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the item')),
                ('remarks', models.TextField(blank=True, help_text='Additional remarks or notes')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'db_table': 'item_master',
                'ordering': ['item_name'],
                'indexes': [models.Index(fields=['category'], name='item_master_categor_5d2586_idx'), models.Index(fields=['status'], name='item_master_status_bd7f46_idx'), models.Index(fields=['classification'], name='item_master_classif_806bc0_idx'), models.Index(fields=['item_name'], name='item_master_item_na_70ce5f_idx')],
            },
        ),
        migrations.CreateModel(
            name='ItemSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=200)),
                ('preference_order', models.PositiveIntegerField(default=1, help_text='1 = Most preferred')),
                ('last_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Last quoted rate from this supplier', max_digits=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_suppliers', to='items.item')),
            ],
            options={
                'db_table': 'item_supplier_mapping',
                'ordering': ['preference_order'],
                'unique_together': {('item', 'supplier_name')},
            },
        ),
    ]
