from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.connector import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    day_id = Column(Integer, ForeignKey("days.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    creator = relationship("User", back_populates="foods")
    day = relationship("Day", back_populates="foods")
    category = relationship("Category", back_populates="foods")
