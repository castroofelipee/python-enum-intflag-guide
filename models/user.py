from sqlalchemy import Column, Integer, String
from enum import IntFlag, auto

from database.db import Base


class UserInfo(IntFlag):
    NONE = 0
    IS_VERIFIED = auto()
    IS_ADMIN = auto()
    IS_BANNED = auto()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    flags = Column(Integer, default=UserInfo.NONE.value)

    def add_flag(self, flag: UserInfo):
        self.flags |= flag

    def remove_flag(self, flag: UserInfo):
        self.flags &= ~flag

    def has_flag(self, flag: UserInfo) -> bool:
        return bool(self.flags & flag)

    def __repr__(self):
        return f"<User username={self.username} flags={self.flags}>"
