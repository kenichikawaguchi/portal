# Generated by Django 5.1.1 on 2024-11-23 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_like_blogpost_alter_like_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='only_friends',
            field=models.BooleanField(default=True, verbose_name='only-friends content?'),
        ),
    ]