# Generated by Django 5.1.4 on 2024-12-29 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_rename_trans_importitem_record_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='importitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]