# Generated by Django 4.0 on 2022-01-04 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypass', '0019_encryptcard_encryptbankaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.BinaryField(max_length=500),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiration',
            field=models.BinaryField(max_length=500),
        ),
        migrations.AlterField(
            model_name='card',
            name='security_code',
            field=models.BinaryField(max_length=500),
        ),
    ]
