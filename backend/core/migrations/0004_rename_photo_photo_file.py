# Generated by Django 4.2.1 on 2023-05-20 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_file_photo_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='photo',
            new_name='file',
        ),
    ]