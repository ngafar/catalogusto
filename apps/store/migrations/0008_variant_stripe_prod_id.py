# Generated by Django 4.1.2 on 2022-10-08 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_stripe_prod_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='stripe_prod_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
