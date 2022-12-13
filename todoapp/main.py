from starlite import Starlite
from starlite.config.cors import CORSConfig
from todoapp.models import connect_db
from .auth import oauth2_auth, auth_router


app = Starlite(
    debug=True,
    route_handlers=[auth_router],
    on_app_init=[oauth2_auth.on_app_init],
    after_startup=[connect_db],
    cors_config=CORSConfig(
        allow_credentials=True,
        allow_origins=[r"*"],
        allow_methods=["*"],
    ),
)
