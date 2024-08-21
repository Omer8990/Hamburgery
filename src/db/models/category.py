from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.connector import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    foods = relationship("Food", back_populates="category")
