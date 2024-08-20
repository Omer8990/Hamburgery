from pydantic import BaseModel


class DayBase(BaseModel):
    day_name: str


class DayCreate(DayBase):
    pass


class DayRead(DayBase):
    day_id: int

    class Config:
        orm_mode = True


class DayUpdate(DayBase):
    pass
