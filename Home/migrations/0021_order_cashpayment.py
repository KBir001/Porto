# Generated by Django 2.2.2 on 2019-08-08 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_cash'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cashpayment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.Cash'),
        ),
    ]
