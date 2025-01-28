from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    """
    Shared fields for Todos.
    """
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)

class TodoCreate(TodoBase):
    """
    Fields required to create a Todo.
    """
    pass

class TodoUpdate(BaseModel):
    """
    Fields allowed to update a Todo.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(Document, TodoBase):
    """
    Beanie model for MongoDB.
    """
    class Settings:
        collection = "todos"  # MongoDB collection name

    class Config:
        # Map MongoDB's `_id` to `id` in responses
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True  # Allows aliasing `_id` to `id`
