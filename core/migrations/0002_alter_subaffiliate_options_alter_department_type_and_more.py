# Generated by Django 5.1.4 on 2024-12-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subaffiliate',
            options={'ordering': ['-subtype'], 'verbose_name': 'تقسيم فرعي', 'verbose_name_plural': 'التقسيمات الفرعية'},
        ),
        migrations.AlterField(
            model_name='department',
            name='type',
            field=models.CharField(choices=[('Department', 'ادارة'), ('Office', 'مكتب'), ('Section', 'قسم'), ('Unit', 'وحدة')], max_length=50, verbose_name='التقسيم الاداري'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='job_title',
            field=models.CharField(choices=[('GM', 'المدير العام'), ('manager', 'مدير'), ('chief', 'رئيس'), ('employee', 'موظف'), ('financer', 'مراقب مالي')], max_length=50, verbose_name='الوظيفة'),
        ),
    ]
