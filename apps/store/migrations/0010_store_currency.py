# Generated by Django 4.1.2 on 2022-10-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_handle'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='currency',
            field=models.CharField(default='usd', max_length=3),
        ),
    ]