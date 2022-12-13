from beanie import Document, Link
from .user import UserInDB


class TodoItem(Document):
    task: str
    completed: bool = False
    owner: Link[UserInDB] | None
