from beanie import PydanticObjectId
from starlite import (
    Controller,
    HTTPException,
    NotFoundException,
    Partial,
    delete,
    get,
    patch,
    post,
    status_codes,
)

from todoapp.models.user import UserInDB

from ..auth import AuthRequest as Request
from ..models.todoitem import TodoItem
from ._utils import BeanieResponse


class TodoItemController(Controller):
    path = "/api/todos"
    response_class = BeanieResponse

    @get("/")
    async def get_todos(self, request: Request) -> list[TodoItem]:
        user_in_db = await UserInDB.find_one(UserInDB.name == request.user.name)
        print(user_in_db)
        result = await TodoItem.find_many(TodoItem.owner.id == user_in_db.id).to_list()
        return result

    @get("/{id:str}")
    async def get_todo(self, id: PydanticObjectId, request: Request) -> TodoItem:
        user_in_db = await UserInDB.find_one(UserInDB.name == request.user.name)
        item = await TodoItem.find_one(
            TodoItem.id == id, TodoItem.owner.id == user_in_db.id
        )

        if item is None:
            raise HTTPException(
                detail="Not Found", status_code=status_codes.HTTP_404_NOT_FOUND
            )

        return item

    @post("/")
    async def create_todo(self, data: TodoItem, request: Request) -> TodoItem:
        user_in_db = await UserInDB.find_one(UserInDB.name == request.user.name)
        if user_in_db is None:
            raise NotFoundException()
        data.owner = user_in_db
        await data.insert()
        del data.owner.password
        return data

    @patch("/{id:str}")
    async def update_todo(self, id: PydanticObjectId, data: Partial[TodoItem], request: Request) -> TodoItem:
        user_in_db = await UserInDB.find_one(UserInDB.name == request.user.name)
        if user_in_db is None:
            raise NotFoundException()
        item_in_db = await TodoItem.find_one(TodoItem.id == id, TodoItem.owner.id == user_in_db.id)
        if item_in_db is None:
            raise NotFoundException()
        update_dict = data.dict(exclude_none=True)
        await item_in_db.set(update_dict)
        return item_in_db

    @delete("/{id:str}")
    async def delete_todo(self, id: PydanticObjectId, request: Request) -> None:
        user_in_db = await UserInDB.find_one(UserInDB.name == request.user.name)
        if user_in_db is None:
            raise NotFoundException()
        item_in_db = await TodoItem.find_one(TodoItem.id == id, TodoItem.owner.id == user_in_db.id)
        if item_in_db is not None:
            await item_in_db.delete()
        # return {"message": "success"}
