# Generated by Django 3.2.12 on 2022-03-26 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprecpro', '0003_merge_0002_comment_follow_like_post_0002_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sprecpro.profile'),
            preserve_default=False,
        ),
    ]
