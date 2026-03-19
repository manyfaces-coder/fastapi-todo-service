from ..base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String


class User(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")

    todos: Mapped[list["Todo"]] = relationship(back_populates="owner")