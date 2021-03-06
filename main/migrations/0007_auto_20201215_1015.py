# Generated by Django 3.1.3 on 2020-12-15 08:15

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20201214_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='overview',
            field=models.TextField(default=2131),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
