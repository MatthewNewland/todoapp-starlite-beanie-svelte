from beanie import Document
from pydantic import BaseModel
from starlite import DTOFactory


class UserOut(BaseModel):
    name: str
    email: str | None


class UserIn(UserOut):
    password: str


class UserInDB(Document, UserIn):
    pass
