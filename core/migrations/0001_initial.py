# Generated by Django 5.1.4 on 2024-12-27 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Ministry', 'وزارة'), ('Authority', 'هيئة'), ('Center', 'مركز'), ('Monitor', 'مراقبة'), ('Project', 'مشروع')], max_length=50, verbose_name='نوع الجهة')),
                ('name', models.CharField(max_length=255, verbose_name='اسم الجهة')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='العنوان')),
            ],
            options={
                'verbose_name': 'جهة',
                'verbose_name_plural': 'الجهات الاخرى',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم الشركة')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='العنوان')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='رقم الهاتف')),
            ],
            options={
                'verbose_name': 'شركة',
                'verbose_name_plural': 'الشركات',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Department', 'ادارة'), ('Office', 'مكتب'), ('Section', 'قسم')], max_length=50, verbose_name='التقسيم الاداري')),
                ('name', models.CharField(max_length=255, verbose_name='اسم التقسيم')),
            ],
            options={
                'verbose_name': 'تقسيم اداري',
                'verbose_name_plural': 'التقسيمات الادارية',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم الموظف')),
                ('job_title', models.CharField(choices=[('GM', 'المدير العام'), ('dept_manager', 'مدير ادارة'), ('offc_manager', 'مدير مكتب'), ('sect_manager', 'رئيس قسم'), ('unit_manager', 'رئيس وحدة'), ('employee', 'موظف'), ('financer', 'مراقب مالي')], max_length=50, verbose_name='الوظيفة')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الالكتروني')),
                ('phone', models.CharField(max_length=15, verbose_name='رقم الهاتف')),
                ('date_employed', models.DateField(verbose_name='تاريخ التعيين')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deptemployees', to='core.department', verbose_name='الادارة/المكتب')),
            ],
            options={
                'verbose_name': 'موظف',
                'verbose_name_plural': 'الموظفين',
                'ordering': ['date_employed'],
            },
        ),
        migrations.CreateModel(
            name='SubAffiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subname', models.CharField(max_length=255, verbose_name='اسم التقسيم')),
                ('subtype', models.CharField(choices=[('Department', 'ادارة'), ('Office', 'مكتب'), ('Section', 'قسم')], max_length=50, verbose_name='التقسيم الاداري')),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subaffiliates', to='core.affiliate')),
            ],
            options={
                'verbose_name': 'جهة',
                'verbose_name_plural': 'الجهات الاخرى',
                'ordering': ['-subtype'],
            },
        ),
    ]
