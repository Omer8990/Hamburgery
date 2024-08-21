from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.db.connector import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))
    vote_value = Column(Integer, nullable=False)

    user = relationship("User", back_populates="votes")
    food = relationship("Food", back_populates="votes")
