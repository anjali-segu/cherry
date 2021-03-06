# Generated by Django 2.0.3 on 2018-07-30 00:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0008_charityprofile_long_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='charityprofile',
            name='tags',
            field=models.ManyToManyField(to='charity.Tag'),
        ),
    ]
