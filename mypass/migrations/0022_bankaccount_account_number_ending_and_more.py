# Generated by Django 4.0 on 2022-01-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypass', '0021_card_card_number_ending'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='account_number_ending',
            field=models.CharField(default=None, max_length=4),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.BinaryField(max_length=500),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='pin_number',
            field=models.BinaryField(max_length=500),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='routing_number',
            field=models.BinaryField(max_length=500),
        ),
    ]
