# Generated by Django 3.2.8 on 2022-10-31 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiofiles', '0005_auto_20221030_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofile',
            name='bitrate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='audiofile',
            name='channels',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='audiofile',
            name='sample_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='audiofile',
            name='sample_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
