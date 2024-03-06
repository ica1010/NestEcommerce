# Generated by Django 3.2 on 2023-11-15 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230921_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='facebook',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='vendor',
            name='instagram',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='vendor',
            name='printerest',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='vendor',
            name='tiktok',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='vendor',
            name='twitter',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='vendor',
            name='youtube',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='cartorderproducts',
            name='product_status',
            field=models.CharField(choices=[('processing', 'Processsing'), ('delivered', 'Delivered'), ('shipped', 'Shipped')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('disabled', 'Disabled'), ('in_review', 'In review'), ('published', 'Published'), ('draft', 'Draft')], default='in_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('disabled', 'Disabled'), ('in_review', 'In review'), ('published', 'Published'), ('draft', 'Draft')], default='in_review', max_length=10),
        ),
    ]