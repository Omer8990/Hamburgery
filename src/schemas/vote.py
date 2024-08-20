from pydantic import BaseModel

class VoteBase(BaseModel):
    user_id: int
    food_id: int

class VoteCreate(VoteBase):
    pass

class VoteRead(VoteBase):
    vote_id: int

    class Config:
        orm_mode = True

class VoteUpdate(VoteBase):
    pass
