from pydantic import BaseModel
from typing import Optional
from datetime import date


class FoodBase(BaseModel):
    name: str
    price: float
    recipe_creator: str
    recipe_creation_date: date
    category: str
    description: Optional[str] = None


class FoodCreate(FoodBase):
    pass


class FoodRead(FoodBase):
    food_id: int

    class Config:
        orm_mode = True


class FoodUpdate(FoodBase):
    pass
