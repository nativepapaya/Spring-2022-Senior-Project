# Generated by Django 3.2.12 on 2022-03-27 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprecpro', '0004_post_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='last_played_uid',
        ),
        migrations.AddField(
            model_name='favorite',
            name='song_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='song_uid',
            field=models.TextField(null=True),
        ),
    ]
