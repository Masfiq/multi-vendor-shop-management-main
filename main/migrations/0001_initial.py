# Generated by Django 3.1.4 on 2021-01-22 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address', models.CharField(max_length=500)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20)),
                ('age_group', models.CharField(choices=[('Young', 'Young'), ('Adult', 'Adult'), ('Old', 'Old')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=3, max_digits=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('status', models.CharField(choices=[('PAID', 'PAID'), ('UNPAID', 'UNPAID')], default='PAID', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('sku', models.CharField(max_length=200, unique=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categories', models.ManyToManyField(related_name='products', to='main.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=30, unique=True)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Sold', 'Sold'), ('Returned', 'Returned'), ('Damaged', 'Damaged')], default=0, max_length=20)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='products', to='main.investor')),
                ('product_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='main.productmodel')),
                ('store', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.store')),
            ],
        ),
        migrations.CreateModel(
            name='OrderUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.productunit')),
            ],
        ),
    ]