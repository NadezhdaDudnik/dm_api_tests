from typing import List, Optional

from pydantic import BaseModel, StrictStr


class InvalidProperties(BaseModel):
    description: [str]


class BadRequestError(BaseModel):
    message: StrictStr
    invalid_properties: Optional[InvalidProperties]
