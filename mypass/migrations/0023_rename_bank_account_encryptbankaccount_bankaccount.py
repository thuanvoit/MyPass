# Generated by Django 4.0 on 2022-01-04 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypass', '0022_bankaccount_account_number_ending_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encryptbankaccount',
            old_name='bank_account',
            new_name='bankaccount',
        ),
    ]
