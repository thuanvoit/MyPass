# Generated by Django 4.0 on 2022-01-03 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypass', '0010_remove_loginhistory_system_version'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginhistory',
            old_name='name',
            new_name='browser',
        ),
        migrations.RemoveField(
            model_name='loginhistory',
            name='system',
        ),
    ]