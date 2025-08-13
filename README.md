# RecipeHub (Django Advanced Project)

Мини уеб приложение за рецепти с публични страници (list/detail), CRUD за логнати потребители, любими, коментари, потребителски колекции и публично API (DRF).

## 🛠 Технологии
- **Python 3.13+**
- **Django 5**
- **PostgreSQL**
- **Django REST Framework**
- **python-dotenv**
- **django-crispy-forms** + **crispy-bootstrap5**
- **Bootstrap 5**

---

## 🚀 Бърз старт (локално)

### 1) Клонирай и влез в проекта
    git clone <repo-url>
    cd recipehub

### 2) Създай и активирай виртуална среда
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS / Linux:
    source .venv/bin/activate

### 3) Инсталирай зависимостите
    pip install -r requirements.txt

### 4) Конфигурация на средата
Копирай `.env.example` като `.env` и попълни стойностите при нужда (SECRET_KEY и данните за PostgreSQL). Примерът в `.env.example` е подходящ за локална разработка.

### 5) Миграции и суперпотребител
    python manage.py migrate
    python manage.py createsuperuser

### 6) Стартирай сървъра
    python manage.py runserver

Отвори в браузър: http://127.0.0.1:8000/

---

## 📌 Основни функционалности
- Регистрация, вход/изход на потребители
- Рецепти: **list / detail / create / edit / delete** (create/edit/delete само за owner или staff)
- **Любими рецепти** (toggle + страница „Моите любими“)
- **Коментари** под рецепти (owner/staff може да изтрива)
- **Потребителски колекции** (list/create/detail + add/remove рецепти)
- **Профил**: преглед + **редакция** (display_name, bio)
- Flash съобщения и Bootstrap 5 UI

---

## 🔐 Достъп и права
- Нелогнат потребител няма достъп до: създаване/редакция/изтриване на рецепти, любими, колекции и техните API endpoint-и.
- Колекциите са видими и управлявани само от собственика (в UI: 404 за чужди; в API: 403 Forbidden).

---

## 📡 API (Django REST Framework)
- **Рецепти (публично)**  
  - Списък: `GET /api/recipes/`  
  - Детайл: `GET /api/recipes/<slug>/`
- **Колекции (само за логнати, само owner)**  
  - Списък/Създаване: `GET/POST /api/collections/`  
  - Детайл/Промяна/Изтриване: `GET/PUT/PATCH/DELETE /api/collections/<pk>/`  
  - Добавяне на рецепта: `POST /api/collections/<pk>/add/`  
    - Тяло (JSON): `{"recipe": <recipe_id>}`  
  - Премахване на рецепта: `DELETE /api/collections/<pk>/remove/<item_id>/`

Пагинация за списъци: `PAGE_SIZE=10`.

---

## 🔗 Полезни URL-и (UI)
- Начало: `/`
- Рецепти: `/recipes/`
- Създай рецепта: `/recipes/create/`
- Любими: `/accounts/favorites/`
- Колекции: `/recipes/collections/`
- Профил: `/accounts/profile/` (редакция: `/accounts/profile/edit/`)
- Админ: `/admin/`

---

