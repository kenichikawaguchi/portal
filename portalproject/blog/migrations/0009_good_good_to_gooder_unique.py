# Generated by Django 5.1.1 on 2024-11-06 14:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_comment_to_good'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='good',
            constraint=models.UniqueConstraint(fields=('good_to_id', 'gooder_id'), name='good_to_gooder_unique'),
        ),
    ]