# Generated by Django 2.2 on 2019-08-03 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20190803_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Cart'),
        ),
    ]