# Generated by Django 4.2.3 on 2023-07-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_product_product_available_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]