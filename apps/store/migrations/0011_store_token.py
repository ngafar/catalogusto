# Generated by Django 4.1.2 on 2022-10-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_store_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='token',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]