# Generated by Django 5.1.1 on 2024-12-14 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20241127_1830'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.category', verbose_name='Category'),
        ),
    ]