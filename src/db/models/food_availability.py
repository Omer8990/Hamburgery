from sqlalchemy import Column, Integer, ForeignKey
from src.db.connector import Base
from sqlalchemy.orm import relationship


class FoodAvailability(Base):
    __tablename__ = "FoodAvailability"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    day_id = Column(Integer, ForeignKey("days.id"))

    food = relationship("Food", back_populates="availability")
    day = relationship("Day", back_populates="availability")
