# Generated by Django 3.2.12 on 2022-11-08 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orderby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.CharField(max_length=30, null=True)),
                ('order_status', models.IntegerField(choices=[(1, 'success'), (2, 'pending'), (0, 'cancel')], default=2, null=True)),
                ('tax', models.FloatField(default=0.18, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Prodect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('model', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(null=True, upload_to='Pictures')),
                ('category', models.CharField(max_length=150, null=True)),
                ('brand', models.CharField(max_length=150, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('stock', models.BooleanField(choices=[(False, 'stockavailable'), (True, 'stockanotvailable')], default=False, help_text='0-Show, 1-Hidden')),
                ('added', models.IntegerField(choices=[(1, 'added_wish'), (2, 'added_cart'), (0, 'not_added')], default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='productname',
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='image',
            field=models.ImageField(null=True, upload_to='cart_img'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.BooleanField(default=False, help_text='0-Add, 1-Remove', null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='order_status',
            field=models.IntegerField(choices=[(1, 'new order'), (2, 'old order'), (0, 'not order'), (3, 'cancel order')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AddField(
            model_name='orderby',
            name='ordered_things',
            field=models.ManyToManyField(null=True, to='shop.Cart'),
        ),
        migrations.AddField(
            model_name='cart',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.prodect'),
        ),
    ]