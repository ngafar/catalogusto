# Generated by Django 4.1.2 on 2022-10-08 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_variants'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='stripe_secret_key',
            field=models.CharField(default='test_key', max_length=55),
            preserve_default=False,
        ),
    ]