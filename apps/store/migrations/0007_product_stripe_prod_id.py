# Generated by Django 4.1.2 on 2022-10-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_store_stripe_secret_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_prod_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]