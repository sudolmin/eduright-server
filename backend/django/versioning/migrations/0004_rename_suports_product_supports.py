# Generated by Django 3.2.4 on 2021-07-25 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('versioning', '0003_product_suports'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='suports',
            new_name='supports',
        ),
    ]
