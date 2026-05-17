from pydantic import BaseModel, Field


class MotorcycleBase(BaseModel):
    model_name: str = Field(min_length=2, max_length=100)
    year: int = Field(ge=1900, le=2100)
    owner_id: int
    category_id: int
    team_id: int | None = None


class MotorcycleCreate(MotorcycleBase):
    pass


class MotorcycleUpdate(BaseModel):
    model_name: str | None = Field(default=None, min_length=2, max_length=100)
    year: int | None = Field(default=None, ge=1900, le=2100)
    owner_id: int | None = None
    category_id: int | None = None
    team_id: int | None = None


class MotorcycleRead(MotorcycleBase):
    id: int

    model_config = {"from_attributes": True}
