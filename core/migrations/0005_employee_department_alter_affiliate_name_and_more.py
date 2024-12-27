# Generated by Django 5.1.4 on 2024-12-25 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_affiliate_options_alter_department_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='core.department', verbose_name='الادارة'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='affiliate',
            name='name',
            field=models.CharField(max_length=255, verbose_name='اسم الجهة'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, verbose_name='اسم الادارة او المكتب'),
        ),
        migrations.AlterField(
            model_name='department',
            name='type',
            field=models.CharField(choices=[('GM', 'المدير العام'), ('Department', 'ادارة'), ('Office', 'مكتب'), ('Section', 'قسم')], max_length=50, verbose_name='نوع التقسيم'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(verbose_name='تاريخ التعيين (yyyy-mm-dd)'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=255, verbose_name='اسم الموظف'),
        ),
    ]
