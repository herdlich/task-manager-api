from datetime import date
from typing import Annotated
from pydantic import BaseModel, StringConstraints

Title = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1)
]


class TaskCreate(BaseModel):
    title: Title
    description: str | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: Title | None = None
    description: str | None = None
    due_date: date | None = None
