# Megano E-Commerce Platform

Полнофункциональный интернет-магазин на Django с REST API и готовым фронтенд-шаблоном.

## Требования

- Python 3.11+
- Django 5.2.9
- DjangoRESTframework 3.16.1

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone <repository>
cd megano
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

### 3. Выполнить миграции
```bash
python manage.py migrate
```

### 4. Создать администратора
```bash
python manage.py createsuperuser
```

### 5. Загрузить тестовые данные (опционально)
```bash
python manage.py create_sample_data
```

### 6. Запустить сервер
```bash
python manage.py runserver 0.0.0.0:8000
```

Сервер будет доступен по адресу `http://localhost:8000`

## Структура проекта

```
megano/
├── api/              # REST API endpoints
├── shop/             # Модели интернет-магазина
├── frontend/         # Фронтенд приложение
├── megano/           # Конфиг проекта
└── manage.py
```

## Основные компоненты

### Модели (shop/models.py)
- **Category** - Категории товаров
- **Product** - Товары
- **ProductPrice** - Цены товаров
- **ProductReview** - Отзывы покупателей
- **Order** - Заказы
- **OrderItem** - Товары в заказе
- **Seller** - Продавцы
- **Banner** - Баннеры на сайте

### API Endpoints

#### Товары
- `GET /api/products/` - Список товаров с фильтрацией и сортировкой
- `GET /api/products/<id>/` - Детали товара
- `GET /api/products/popular/` - Популярные товары (8 штук)
- `GET /api/products/limited/` - Товары с ограниченным тиражом
- `GET /api/products/<id>/reviews/` - Отзывы товара
- `POST /api/products/<id>/add_review/` - Добавить отзыв (требуется авторизация)

#### Категории
- `GET /api/categories/` - Список категорий

#### Баннеры
- `GET /api/banners/` - Список баннеров

#### Заказы (требуется авторизация)
- `GET /api/orders/` - Мои заказы
- `POST /api/orders/` - Создать новый заказ
- `GET /api/orders/<id>/` - Детали заказа
- `POST /api/orders/<id>/pay/` - Оплатить заказ

## Фильтрация и сортировка

### Параметры фильтрации товаров
- `?category=<id>` - Фильтр по категории
- `?search=<text>` - Поиск по названию и описанию

### Параметры сортировки
- `?ordering=sort_index` - По индексу сортировки (возрастание)
- `?ordering=-sort_index` - По индексу сортировки (убывание)
- `?ordering=price` - По цене (возрастание)
- `?ordering=-price` - По цене (убывание)
- `?ordering=review_count` - По количеству отзывов
- `?ordering=id` - По дате добавления

## Админ-панель

Доступна по адресу `/admin/`
- Логин: `admin`
- Пароль: `123456` (по умолчанию, измените после запуска)

## Авторизация в API

Для доступа к защищенным endpoint'ам (заказы) используйте Token Authentication:

```bash
POST /api-auth/login/ - Получить токен
```

Затем передавайте токен в заголовке:
```
Authorization: Token <your_token>
```

## Тестовые данные

После выполнения команды `python manage.py create_sample_data` будут созданы:
- Продавцы (TechStore, ElectroShop)
- Категории (Electronics, Computers, Phones)
- 5 тестовых товаров
- Тестовый пользователь (username: testuser, password: 123456)
- Тестовые отзывы

## Миграции

Все миграции находятся в папке `shop/migrations/`. 
Для откатывания миграций используйте:

```bash
python manage.py migrate shop 0001_initial
```

## Развертывание

Для production используйте gunicorn:

```bash
gunicorn megano.wsgi:application --bind 0.0.0.0:8000
```

## Лицензия

MIT
