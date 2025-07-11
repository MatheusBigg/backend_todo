from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoSchema(BaseModel):
    title: str
    description: str | None = None
    state: TodoState = Field(default=TodoState.todo)


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]
