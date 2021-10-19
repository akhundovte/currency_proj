### currency
 

**Запуск проекта**  

- Переход в папку с файлом docker-compose.yml  
```console
cd deploy/currency
``` 

- Создание образов  
```console
docker-compose build
```

- Запуск контейнеров  
```console
docker-compose up -d
```

- Применение миграций  
```console
docker-compose exec currency_test python manage.py migrate
```

- Загрузка данных из внешнего источника  
```console
docker-compose exec currency_test python manage.py loadcurrencies
```

**Адрес в браузере**  
http://localhost:8080  
