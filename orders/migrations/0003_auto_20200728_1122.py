# Generated by Django 3.0.8 on 2020-07-28 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200727_1051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered',
            new_name='is_ordered',
        ),
    ]
