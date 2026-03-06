from datetime import datetime as dt
from typing import List
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SpaceType(Base):
    __tablename__ = "space_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    logs: Mapped[List["Logs"]] = relationship("Logs", back_populates="space_type")


class EventType(Base):
    __tablename__ = "event_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    logs: Mapped[List["Logs"]] = relationship("Logs", back_populates="event_type")


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    datetime: Mapped[dt] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    space_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("space_type.id"), nullable=False
    )
    event_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event_type.id"), nullable=False
    )

    space_type: Mapped["SpaceType"] = relationship("SpaceType", back_populates="logs")
    event_type: Mapped["EventType"] = relationship("EventType", back_populates="logs")
