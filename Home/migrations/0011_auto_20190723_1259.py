# Generated by Django 2.2.2 on 2019-07-23 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_men_sleeve'),
    ]

    operations = [
        migrations.AddField(
            model_name='men',
            name='color',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='men',
            name='febric',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='men',
            name='necktype',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
