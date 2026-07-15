from datetime import date
from typing import Annotated
from pydantic import (
    BaseModel,
    ConfigDict,
    StringConstraints,
    field_validator,
)

Title = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1)
]


class TaskBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskCreate(BaseModel):
    title: Title
    description: str | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: Title | None = None
    description: str | None = None
    due_date: date | None = None

    @field_validator("title", mode="before")
    @classmethod
    def reject_null_title(cls, value: object) -> object:
        if value is None:
            raise ValueError("title cannot be null")
        return value


class TaskResponse(BaseModel):
    id: int
    title: Title
    description: str | None
    due_date: date | None
