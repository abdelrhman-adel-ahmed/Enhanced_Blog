# Generated by Django 3.1.3 on 2020-12-13 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]