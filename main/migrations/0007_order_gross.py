# Generated by Django 3.1.4 on 2021-01-23 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210123_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gross',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
            preserve_default=False,
        ),
    ]
