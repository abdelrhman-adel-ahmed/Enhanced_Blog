# Generated by Django 3.1.3 on 2020-12-13 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_post_featured'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='timestamo',
            new_name='timestamp',
        ),
    ]
