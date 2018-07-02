# Generated by Django 2.0.3 on 2018-07-01 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0004_campaign_campaignitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignitem',
            name='item_cost',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaignitem',
            name='item_description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='campaignitem',
            name='item_img_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='campaignitem',
            name='item_name',
            field=models.CharField(default='example', max_length=100),
            preserve_default=False,
        ),
    ]
