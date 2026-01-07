from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal, init_db
from models import User, UserInfo
from schemas import UserCreate, UserOut

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(username=payload.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/users/{user_id}/flags/{flag_name}")
def add_flag(user_id: int, flag_name: str, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    try:
        flag = UserInfo[flag_name]
    except KeyError:
        raise HTTPException(400, "Invalid flag name")

    user.add_flag(flag)
    db.commit()

    return {"message": f"Flag {flag_name} added", "flags": user.flags}


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
