# Generated by Django 5.0.2 on 2024-02-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20240218_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('draft', 'Draft'), ('rejected', 'Rejected'), ('published', 'Published'), ('in_review', 'In review')], default='in_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('draft', 'Draft'), ('rejected', 'Rejected'), ('published', 'Published'), ('in_review', 'In review')], default='in_review', max_length=10),
        ),
    ]
