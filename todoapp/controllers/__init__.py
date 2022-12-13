from starlite import Router, Provide
from todoapp.auth import current_active_user
from .todoitem import TodoItemController

controller_router = Router(
    "/",
    dependencies={"user": Provide(current_active_user)},
    route_handlers=[TodoItemController],
)
