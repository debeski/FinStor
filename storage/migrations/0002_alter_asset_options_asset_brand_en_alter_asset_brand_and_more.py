# Generated by Django 5.1.4 on 2024-12-28 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ['-category'], 'verbose_name': 'صنف', 'verbose_name_plural': 'اصناف'},
        ),
        migrations.AddField(
            model_name='asset',
            name='brand_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Brand in English'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='brand',
            field=models.CharField(blank=True, max_length=255, verbose_name='العلامة بالعربية'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='storage.assetcategory', verbose_name='التصنيف'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='اسم الصنف'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='unit',
            field=models.CharField(choices=[('piece', 'قطعة'), ('box', 'علبة')], default='piece', max_length=50, verbose_name='وحدة القياس'),
        ),
        migrations.AlterField(
            model_name='assetcategory',
            name='discription',
            field=models.CharField(blank=True, max_length=255, verbose_name='التفاصيل...'),
        ),
        migrations.AlterField(
            model_name='assetcategory',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='اسم التصنيف'),
        ),
    ]