# Generated by Django 3.0.9 on 2020-08-04 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_checkoutaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.CheckoutAddress'),
        ),
    ]
