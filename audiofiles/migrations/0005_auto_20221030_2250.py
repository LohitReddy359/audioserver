# Generated by Django 3.2.8 on 2022-10-30 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiofiles', '0004_alter_audiofile_binary_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audiofile',
            old_name='binary_data',
            new_name='audio_file',
        ),
        migrations.AddField(
            model_name='audiofile',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
