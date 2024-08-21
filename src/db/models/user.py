from sqlalchemy import Column, Integer, String
from src.db.connector import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    foods = relationship("Food", back_populates="creator")
    votes = relationship("Vote", back_populates="user")
