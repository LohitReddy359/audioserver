# Generated by Django 3.2.8 on 2022-10-31 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiofiles', '0006_auto_20221031_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
