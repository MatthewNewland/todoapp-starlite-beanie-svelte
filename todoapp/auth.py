from datetime import timedelta
from os import environ
from passlib.hash import bcrypt
from typing import Any
from starlite import (
    ASGIConnection,
    HTTPException,
    Provide,
    Request,
    Response,
    status_codes,
    Router,
    post,
)
from starlite.config import AppConfig
from starlite.contrib.jwt import JWTAuth, Token
from .models.user import UserInDB, UserIn, UserOut


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection
) -> UserOut | None:
    cached_value = await connection.cache.get(token.sub)
    if cached_value:
        return UserOut(**cached_value)
    return None


jwt_auth = JWTAuth[UserInDB](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=environ.get("JWT_SECRET", "abcd123"),
    token_url="/auth/token",
    exclude=["/auth/login", "/auth/create-user", "/auth/token", "/schema"],
    default_token_expiration=timedelta(days=365),
)


@post("/create-user")
async def create_user_handler(data: UserIn) -> UserOut:
    if await UserInDB.find({UserInDB.name: data.name}).count() > 0:
        raise HTTPException(
            detail="User already exists", status_code=status_codes.HTTP_403_FORBIDDEN
        )

    hash = bcrypt.hash(data.password)
    user_for_db = UserInDB(**data.dict(exclude={"password"}), password=hash)

    await user_for_db.insert()
    return user_for_db.dict(exclude={"id", "password"})


@post("/login")
async def login_handler(request: Request[Any, Any], data: UserIn) -> Response[UserInDB]:
    user_in_db = await UserInDB.find({UserInDB.name: data.name}).first_or_none()
    if user_in_db is None and data.email is not None:
        user_in_db = await UserInDB.find({UserInDB.email: data.email}).first_or_none()
    if user_in_db is None:
        raise HTTPException(
            detail="Username does not exist",
            status_code=status_codes.HTTP_403_FORBIDDEN,
        )

    valid_password = bcrypt.verify(
        data.password, user_in_db.password.get_secret_value()
    )

    if not valid_password:
        raise HTTPException(
            detail="Username and password do not match",
            status_code=status_codes.HTTP_401_UNAUTHORIZED,
        )

    await request.cache.set(str(user_in_db.id), user_in_db.dict())
    response = jwt_auth.login(
        identifier=str(user_in_db.id),
        response_body=user_in_db.dict(exclude={"id", "password"}),
    )
    return response


@post("/token")
async def token_handler(request: Request[Any, Any]) -> dict[str, str]:
    name, password = request.headers["authorization"].split(":")
    data = UserIn(name=name, email=name, password=password)
    user_in_db = await UserInDB.find({UserInDB.name: data.name}).first_or_none()
    if user_in_db is None and data.email is not None:
        user_in_db = await UserInDB.find({UserInDB.email: data.email}).first_or_none()
    if user_in_db is None:
        raise HTTPException(
            detail="Username does not exist",
            status_code=status_codes.HTTP_403_FORBIDDEN,
        )

    valid_password = bcrypt.verify(
        data.password, user_in_db.password.get_secret_value()
    )

    if not valid_password:
        raise HTTPException(
            detail="Username and password do not match",
            status_code=status_codes.HTTP_401_UNAUTHORIZED,
        )

    await request.cache.set(str(user_in_db.id), user_in_db.dict())
    token = jwt_auth.create_token(
        str(user_in_db.id), token_expiration=timedelta(days=30)
    )
    return {
        "access_token": token,
        "userOut": user_in_db.dict(exclude={"password", "id"}),
    }


def on_app_init(app_config: AppConfig) -> AppConfig:
    if app_config.debug:
        return app_config
    return jwt_auth.on_app_init(app_config)


AuthRequest = Request[UserInDB, JWTAuth]


async def current_active_user(request: AuthRequest) -> UserInDB:
    if request.app.debug:
        user_in_db = await UserInDB.find_one(UserInDB.name == "mnewland")
        return user_in_db
    user_in_db = await UserInDB.find_one(UserInDB.name == request.user.name)
    return user_in_db


@post("/logout", dependencies={"user": Provide(current_active_user)})
async def logout_handler(request: AuthRequest, user: UserInDB) -> dict[str, str]:
    await request.cache.delete(str(user.id))
    return {"message": "successfully logged out"}


auth_router = Router(
    "/auth",
    route_handlers=[login_handler, create_user_handler, token_handler, logout_handler],
)
