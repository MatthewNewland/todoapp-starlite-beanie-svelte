from os import environ
from passlib.hash import bcrypt
from typing import Any
from starlite import (
    ASGIConnection,
    HTTPException,
    Request,
    Response,
    status_codes,
    Router,
    post,
)
from starlite.contrib.jwt import OAuth2PasswordBearerAuth, Token
from .models.user import UserInDB, UserIn, UserOut


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection
) -> UserOut | None:
    cached_value = await connection.cache.get(token.sub)
    if cached_value:
        return UserOut(**cached_value)
    return None


oauth2_auth = OAuth2PasswordBearerAuth(
    retrieve_user_handler=retrieve_user_handler,
    token_secret=environ.get("JWT_SECRET", "abcd123"),
    token_url="/auth/login",
    exclude=["/auth/login", "/auth/create-user", "/schema"],
)


@post("/create-user")
async def create_user_handler(data: UserIn) -> UserOut:
    if await UserInDB.find({UserInDB.name: data.name}).count() > 0:
        raise HTTPException(
            detail="User already exists", status_code=status_codes.HTTP_403_FORBIDDEN
        )

    hash = bcrypt.hash(data.password)
    user_for_db = UserInDB(**data.dict(exclude={"password"}), password=hash)

    await user_for_db.save()
    return user_for_db.dict(exclude={"password", "id"})


@post("/login")
async def login_handler(request: Request[Any, Any], data: UserIn) -> Response[UserOut]:
    user_in_db = await UserInDB.find({UserInDB.name: data.name}).first_or_none()
    if user_in_db is None and data.email is not None:
        user_in_db = await UserInDB.find({UserInDB.email: data.email}).first_or_none()
    if user_in_db is None:
        raise HTTPException(
            detail="Username does not exist",
            status_code=status_codes.HTTP_403_FORBIDDEN,
        )

    valid_password = bcrypt.verify(data.password, user_in_db.password)

    if not valid_password:
        raise HTTPException(
            detail="Username and password do not match",
            status_code=status_codes.HTTP_401_UNAUTHORIZED,
        )

    await request.cache.set(str(user_in_db.name), user_in_db.dict())
    response = oauth2_auth.login(
        identifier=str(user_in_db.id),
        response_body=user_in_db.dict(exclude={"password", "id"}),
    )
    return response


auth_router = Router("/auth", route_handlers=[login_handler, create_user_handler])
