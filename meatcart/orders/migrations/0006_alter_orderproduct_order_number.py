# Generated by Django 4.2.3 on 2023-08-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderproduct_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
