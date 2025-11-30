from fastapi import FastAPI, Depends, HTTPException, status, Request, Form  # ← 新增 Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
import models
import schemas
import security
import database
import redis_client

app = FastAPI(title="Сервис аутентификации")

# Создание таблиц в базе данных при запуске
models.Base.metadata.create_all(bind=database.engine)

# Зависимость для получения сессии базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Настройка механизма авторизации через Bearer-токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Получение текущего пользователя по токену из заголовка Authorization
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Недействительный токен")
    if redis_client.is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Токен отозван")
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user

# 1. Регистрация нового пользователя (принимает JSON)
@app.post("/register", status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Электронная почта уже зарегистрирована")
    hashed_pw = security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "Пользователь создан"}

# 2. Вход через форму (поддерживает Swagger UI — и Authorize, и Execute!)
@app.post("/login", response_model=schemas.Token)
def login(
    username: str = Form(...),      # ← 关键修改：显式声明表单字段
    password: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    # form_data.username на самом деле содержит email
    db_user = db.query(models.User).filter(models.User.email == username).first()
    if not db_user or not security.verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    # Сохранение истории входа (если доступен запрос)
    if request:
        history = models.LoginHistory(
            user_id=db_user.id,
            user_agent=request.headers.get("user-agent", "")
        )
        db.add(history)
        db.commit()

    access_token = security.create_access_token(data={"sub": db_user.email})
    refresh_token = security.create_refresh_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# 2b. Вход через JSON (для фронтенда или мобильного клиента)
@app.post("/login/json", response_model=schemas.Token)
def login_json(credentials: schemas.LoginJson, request: Request = None, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not db_user or not security.verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    # Сохранение истории входа
    if request:
        history = models.LoginHistory(
            user_id=db_user.id,
            user_agent=request.headers.get("user-agent", "")
        )
        db.add(history)
        db.commit()

    access_token = security.create_access_token(data={"sub": db_user.email})
    refresh_token = security.create_refresh_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# 3. Обновление access-токена с помощью refresh-токена
@app.post("/refresh", response_model=schemas.Token)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    payload = security.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Недействительный refresh-токен")
    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    new_access = security.create_access_token(data={"sub": email})
    new_refresh = security.create_refresh_token(data={"sub": email})
    return {"access_token": new_access, "refresh_token": new_refresh}

# 4. Обновление данных пользователя (email или пароль)
@app.put("/user/update")
def update_user(update: schemas.UserUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if update.email:
        current_user.email = update.email
    if update.password:
        current_user.hashed_password = security.get_password_hash(update.password)
    db.commit()
    return {"msg": "Данные обновлены"}

# 5. Получение истории входов текущего пользователя
@app.get("/user/history", response_model=list[schemas.LoginHistoryEntry])
def get_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(models.LoginHistory).filter(models.LoginHistory.user_id == current_user.id).all()
    return history

# 6. Выход из системы (добавление токена в чёрный список Redis)
@app.post("/logout")
def logout(request: Request, current_user: models.User = Depends(get_current_user)):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        # Токен блокируется на 15 минут (900 секунд)
        redis_client.add_token_to_blacklist(token, 900)
    return {"msg": "Выполнен выход из системы"}