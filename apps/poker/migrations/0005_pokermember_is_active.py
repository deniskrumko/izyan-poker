# Generated by Django 2.2.4 on 2020-01-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0004_auto_20200114_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokermember',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
    ]