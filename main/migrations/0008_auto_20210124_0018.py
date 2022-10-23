# Generated by Django 3.1.4 on 2021-01-23 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_order_gross'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.productmodel'),
        ),
    ]