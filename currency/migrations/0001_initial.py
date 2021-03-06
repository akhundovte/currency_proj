# Generated by Django 2.2 on 2021-10-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('rate', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Курс к рублю')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
                'db_table': 'currency',
            },
        ),
    ]
