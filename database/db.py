from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from models import user

DATABASE = "sqlite:///tutorial.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE, echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
