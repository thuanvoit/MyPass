# Generated by Django 4.0 on 2022-01-03 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypass', '0011_rename_name_loginhistory_browser_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoginHistory',
        ),
    ]
