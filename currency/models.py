from django.db import models


class Currency(models.Model):
    code = models.CharField(verbose_name='Код', max_length=3, unique=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Курс к рублю')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        db_table = 'currency'
