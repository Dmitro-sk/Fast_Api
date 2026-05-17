from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=50)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    country: str | None = Field(default=None, min_length=2, max_length=50)


class TeamRead(TeamBase):
    id: int

    model_config = {"from_attributes": True}
