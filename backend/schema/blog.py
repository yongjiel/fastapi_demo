from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import root_validator


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    @root_validator(pre=True)
    def generate_slug(cls, values):
        if "slug" in values:
            return values
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class ShowBlog(BaseModel):
    id: int
    title: str
    slug: str
    author_id: int
    content: Optional[str]
    created_at: date

    class Config:
        orm_mode = True


class UpdateBlog(CreateBlog):
    pass
