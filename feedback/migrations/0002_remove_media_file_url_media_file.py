# Generated by Django 5.1.6 on 2025-03-26 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='file_url',
        ),
        migrations.AddField(
            model_name='media',
            name='file',
            field=models.FileField(default="''", upload_to='feedback_media/'),
            preserve_default=False,
        ),
    ]
