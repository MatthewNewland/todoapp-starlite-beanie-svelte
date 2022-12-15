from beanie import init_beanie
from starlite.config.app import AppConfig
from .user import UserInDB
from .todoitem import TodoItem


async def connect_db(app_config: AppConfig):
    await init_beanie(
        connection_string="mongodb://localhost:27017/todoapp",
        document_models=[UserInDB, TodoItem]
    )
    return app_config
