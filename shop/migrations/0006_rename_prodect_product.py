# Generated by Django 3.2.12 on 2022-11-08 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_wishlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prodect',
            new_name='product',
        ),
    ]
