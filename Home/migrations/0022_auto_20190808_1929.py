# Generated by Django 2.2.2 on 2019-08-08 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0021_order_cashpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cashpayment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.Cash'),
        ),
    ]
