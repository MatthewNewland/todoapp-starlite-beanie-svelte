from starlite import Starlite
from starlite.config.cors import CORSConfig
from starlite.config.openapi import OpenAPIConfig
from todoapp.models import connect_db
from .auth import oauth2_auth, auth_router
from .controllers import controller_router


app = Starlite(
    debug=True,
    route_handlers=[auth_router, controller_router],
    on_app_init=[oauth2_auth.on_app_init],
    after_startup=[connect_db],
    cors_config=CORSConfig(
        allow_credentials=True,
        allow_origins=[r"*"],
        allow_methods=["*"],
    ),
    openapi_config=OpenAPIConfig(
        title="Todo API",
        version="0.1.0"
    )
)
