# Generated by Django 3.2.12 on 2022-04-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprecpro', '0007_auto_20220404_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='edited_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
