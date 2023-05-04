# Generated by Django 4.0 on 2022-01-04 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mypass', '0016_encryptcontent_delete_passwordencrypt'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=500)),
                ('password', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encrypt_password', to='mypass.password')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_encrypt_pass', to='mypass.user')),
            ],
        ),
        migrations.DeleteModel(
            name='EncryptContent',
        ),
    ]
