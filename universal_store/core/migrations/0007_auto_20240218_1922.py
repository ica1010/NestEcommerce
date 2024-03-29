# Generated by Django 3.2.24 on 2024-02-18 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20231115_2145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-date',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='cartorderproducts',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cartorderproducts',
            name='product_status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('delivered', 'Delivered'), ('processing', 'Processsing')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('in_review', 'In review'), ('disabled', 'Disabled'), ('published', 'Published'), ('draft', 'Draft')], default='in_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('in_review', 'In review'), ('disabled', 'Disabled'), ('published', 'Published'), ('draft', 'Draft')], default='in_review', max_length=10),
        ),
    ]
