# Generated by Django 5.1.1 on 2025-01-15 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_category_category_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=32, verbose_name='IP Address')),
                ('page', models.CharField(max_length=32, verbose_name='Access Page')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
        ),
    ]