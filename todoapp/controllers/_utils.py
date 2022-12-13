from typing import Any

from beanie import PydanticObjectId, Link
from starlite import Response
from ..models import UserInDB


class BeanieResponse(Response):
    def serializer(self, value: Any) -> dict[str, Any]:
        if isinstance(value, PydanticObjectId):
            return str(value)
        if isinstance(value, Link):
            return value.to_dict().get("id")
        if isinstance(value, UserInDB):
            return value.dict(exclude={'password'})

        return super().serializer(value)
