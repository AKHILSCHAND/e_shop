# Generated by Django 4.2.5 on 2023-09-10 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]