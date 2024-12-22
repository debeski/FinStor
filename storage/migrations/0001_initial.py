# Generated by Django 5.1.4 on 2024-12-22 08:45

import django.db.models.deletion
import storage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('association', models.CharField(choices=[('Ministry', 'Ministry'), ('Department', 'Department'), ('Office', 'Office')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Car', 'Car'), ('Electronic', 'Electronic'), ('Computer', 'Computer'), ('Hardware', 'Hardware'), ('Printers', 'Printers'), ('Office', 'Office'), ('Appliance', 'Appliance'), ('Electrical', 'Electrical'), ('Equipment', 'Equipment'), ('Furniture', 'Furniture'), ('Cleaner', 'Cleaner'), ('Food', 'Food'), ('Other', 'Other')], max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('GM', 'General Management'), ('Department', 'Department'), ('Office', 'Office'), ('Section', 'Section')], max_length=50)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('date_employed', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ExportRecord',
            fields=[
                ('trans_id', models.AutoField(primary_key=True, serialize=False)),
                ('export_type', models.CharField(choices=[('Consume', 'Consume'), ('Personal', 'Personal'), ('Department', 'Department'), ('Loan', 'Loan')], max_length=50)),
                ('entity_object_id', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='ExportItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('sn', models.CharField(blank=True, max_length=100, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='media/export_item_pics/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('return_at', models.DateTimeField(blank=True, null=True)),
                ('return_purpose', models.CharField(blank=True, choices=[('EndJob', 'End Job'), ('Stolen', 'Stolen'), ('NoReason', 'No Reason')], max_length=50, null=True)),
                ('return_condition', models.CharField(blank=True, choices=[('Good', 'Good'), ('Bad', 'Bad'), ('Dead', 'Dead')], max_length=50, null=True)),
                ('return_notes', models.TextField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.asset')),
                ('trans_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='storage.exportrecord')),
            ],
        ),
        migrations.CreateModel(
            name='ImportRecord',
            fields=[
                ('trans_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('assign_number', models.CharField(max_length=50)),
                ('assign_date', models.DateField()),
                ('notes', models.TextField()),
                ('pdf_file', models.FileField(blank=True, upload_to=storage.models.get_pdf_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.company')),
            ],
        ),
        migrations.CreateModel(
            name='ImportItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('return_at', models.DateTimeField(blank=True, null=True)),
                ('return_purpose', models.CharField(blank=True, choices=[('Damaged', 'Damaged'), ('Replace', 'Replace')], max_length=50, null=True)),
                ('return_notes', models.TextField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.asset')),
                ('trans_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='storage.importrecord')),
            ],
        ),
    ]
