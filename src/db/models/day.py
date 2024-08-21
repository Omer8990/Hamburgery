from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.connector import Base


class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    availability = relationship("FoodAvailability", back_populates="day")
