# Generated by Django 3.1.4 on 2021-01-23 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210123_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='phone',
            field=models.CharField(default='01828442772', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
