# Generated by Django 4.2.10 on 2024-02-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_cartorderproducts_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderproducts',
            name='product_status',
            field=models.CharField(choices=[('processing', 'Processsing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='notification',
            name='receptor',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('in_review', 'In review'), ('draft', 'Draft'), ('rejected', 'Rejected'), ('published', 'Published')], default='in_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('in_review', 'In review'), ('draft', 'Draft'), ('rejected', 'Rejected'), ('published', 'Published')], default='in_review', max_length=10),
        ),
    ]
