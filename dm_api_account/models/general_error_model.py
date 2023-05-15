from __future__ import annotations
from pydantic import BaseModel, StrictStr, Extra, Field
from typing import Optional


class GeneralError(BaseModel):
    class Config:
        extra = Extra.forbid

    message: Optional[StrictStr] = Field(None, description='Client message')
