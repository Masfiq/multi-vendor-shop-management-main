# Generated by Django 3.1.4 on 2021-01-30 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210124_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='profit_lifetime',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='investor',
            name='balance',
            field=models.DecimalField(decimal_places=3, max_digits=30),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='price_sold',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='profit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Sold', 'Sold')], default='Available', max_length=20),
        ),
    ]