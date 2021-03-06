# Generated by Django 2.2 on 2019-08-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20190803_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('self', 'Самовывоз'), ('delivery', 'Доставка')], default='Самовывоз', max_length=40),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Обработка', 'Обработка'), ('Выполняется', 'Выполняется'), ('Оплачен', 'Оплачен')], default='Обработка', max_length=60),
        ),
    ]
