# Generated by Django 3.1.3 on 2020-11-21 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['pk'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]