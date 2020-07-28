# Generated by Django 3.0.8 on 2020-07-27 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='start_date',
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]