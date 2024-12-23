# Generated by Django 5.1.4 on 2024-12-22 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='affiliate',
            options={'ordering': ['-association'], 'verbose_name': 'الجهة', 'verbose_name_plural': 'الجهات'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'الشركة', 'verbose_name_plural': 'الشركات'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name'], 'verbose_name': 'الادارة', 'verbose_name_plural': 'الادارات'},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['name'], 'verbose_name': 'الموظف', 'verbose_name_plural': 'الموظفين'},
        ),
    ]
