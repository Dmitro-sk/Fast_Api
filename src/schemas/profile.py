from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    bio: str | None = None
    experience_years: int = Field(default=0, ge=0, le=80)
    user_id: int


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    bio: str | None = None
    experience_years: int | None = Field(default=None, ge=0, le=80)


class ProfileRead(ProfileBase):
    id: int

    model_config = {"from_attributes": True}
