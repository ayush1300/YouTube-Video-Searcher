# Generated by Django 3.1.5 on 2021-01-06 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videos',
            old_name='url',
            new_name='videoId',
        ),
    ]