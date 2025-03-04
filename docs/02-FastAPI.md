# Вступ до FastAPI

## 1. Що таке FastAPI?
**FastAPI** — це сучасний, швидкий (як випливає з назви) фреймворк для створення API на Python.  
Його основні переваги:
- Простий у використанні.
- Використовує **Pydantic** для валідації даних.
- Автоматично генерує документацію Swagger UI та ReDoc.

## 2. Встановлення FastAPI
Щоб встановити FastAPI та сервер Uvicorn, виконайте команду:
```sh
pip install fastapi uvicorn
```

## 3. Створення першого маршруту
Спочатку створимо простий FastAPI-додаток:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

Запустити сервер можна командою:
```sh
uvicorn main:app --reload
```
Перевірити роботу можна у браузері за адресою:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)  

Автоматична документація доступна за адресами:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 4. Використання `APIRouter` для маршрутизації
У великих додатках краще використовувати **APIRouter** для розбиття API на модулі.

### 4.1. Створення файлу `routes/users.py`:
```python
from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("/")
def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}
```

### 4.2. Реєстрація маршруту у `main.py`:
```python
from fastapi import FastAPI
from routes.users import router as users_router

app = FastAPI()
app.include_router(users_router)
```

Тепер запити до `/users` і `/users/{id}` будуть оброблятися окремим маршрутизатором.

---

## 5. HTTP-методи у FastAPI (CRUD)
FastAPI підтримує стандартні HTTP-методи: **GET, POST, PUT, DELETE**.

### 5.1. CRUD для користувачів (`routes/users.py`)
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users")

# Модель користувача
class User(BaseModel):
    name: str
    age: int

# Фейкова база даних
users_db = []

@router.post("/")
def create_user(user: User):
    new_user = {"id": len(users_db) + 1, "name": user.name, "age": user.age}
    users_db.append(new_user)
    return new_user

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    for u in users_db:
        if u["id"] == user_id:
            u.update(user.model_dump())
            return u
    return {"error": "User not found"}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]
    return {"message": "User deleted"}
```

---

## 6. Використання параметрів у запитах

### 6.1. Шляхові параметри
```python
@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "message": f"User {user_id}"}
```
Запит: `GET /users/1` → `{"id": 1, "message": "User 1"}`

### 6.2. Параметри запиту
```python
@router.get("/")
def get_users(limit: int = 10, offset: int = 0):
    return {"message": f"Returning {limit} users starting from {offset}"}
```
Запит: `GET /users?limit=5&offset=10`

---

## 7. Повернення статус-кодів та заголовків
```python
from fastapi import HTTPException

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id > len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id - 1]
```
Запит `GET /users/100` поверне:
```json
{
    "detail": "User not found"
}
```

---

## 8. Аутентифікація за допомогою токенів
FastAPI підтримує аутентифікацію через **Bearer Token**.

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@router.get("/secure")
def secure_route(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if token != "secret-token":
        raise HTTPException(status_code=403, detail="Invalid token")
    return {"message": "Access granted"}
```
Запит:
```
GET /users/secure
Authorization: Bearer secret-token
```

---

## 9. Запуск FastAPI у режимі production
Для production використовують Gunicorn + Uvicorn:
```sh
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

---