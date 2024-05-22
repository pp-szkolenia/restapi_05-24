from pydantic import BaseModel
from enum import Enum


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_complete: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class TaskResponse(BaseModel):
    id_: int
    description: str
    priority: int | None = None
    is_complete: bool


class GetSingleTaskResponse(BaseModel):
    result: TaskResponse


class GetAllTasksResponse(BaseModel):
    result: list[TaskResponse]


class PostTaskResponse(BaseModel):
    message: str
    details: TaskResponse


class PostTaskNoDetailsResponse(BaseModel):
    message: str


class PutTaskResponse(BaseModel):
    message: str
    new_value: TaskResponse


class UserResponse(BaseModel):
    id_: int
    username: str
    password: str
    is_admin: bool


class GetSingleUserResponse(BaseModel):
    result: UserResponse


class GetAllUsersResponse(BaseModel):
    result: list[UserResponse]


class PostUserResponse(BaseModel):
    message: str
    details: UserResponse


class PutUserResponse(BaseModel):
    message: str
    new_value: UserResponse


class PutUserNoValueResponse(BaseModel):
    message: str


class SortOrders(Enum):
    ASC = "asc"
    DESC = "desc"


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    is_admin: bool
