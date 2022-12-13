from beanie import init_beanie
from .user import UserInDB


async def connect_db(app_config):
    await init_beanie(
        connection_string="mongodb://localhost:27017/todoapp",
        document_models=[UserInDB]
    )
    return app_config
