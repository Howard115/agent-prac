from pydantic import BaseModel, Field
from typing import Union


class LocationMapResponse(BaseModel):
    location: Union[str, None] = Field(
        default=None,
        description="The location to create a map for (include country name)"
    )
    response: str = Field(
        default="I can help you find locations on the map!",
        description="Response message to the user"
    )