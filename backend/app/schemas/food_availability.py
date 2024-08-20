from pydantic import BaseModel

class FoodAvailabilityBase(BaseModel):
    food_id: int
    day_id: int

class FoodAvailabilityCreate(FoodAvailabilityBase):
    pass

class FoodAvailabilityRead(FoodAvailabilityBase):
    food_availability_id: int

    class Config:
        orm_mode = True

class FoodAvailabilityUpdate(FoodAvailabilityBase):
    pass
