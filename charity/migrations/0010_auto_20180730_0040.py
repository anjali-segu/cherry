# Generated by Django 2.0.3 on 2018-07-30 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0009_auto_20180730_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
