from __future__ import annotations
from typing import List, Optional, Dict
from pydantic import BaseModel, StrictStr, Extra, Field


class Errors(BaseModel):
    class Config:
        extra = Extra.forbid

    Email: Optional[Dict[str, List[StrictStr]]] = Field(None, description='Email')
    Login: Optional[Dict[str, List[StrictStr]]] = Field(None, description='Login')
    Password: Optional[Dict[str, List[StrictStr]]] = Field(None, description='Password')
    login: Optional[List] = Field(None, description='Login')


class BadRequestError(BaseModel):
    class Config:
        extra = Extra.forbid

    message: Optional[StrictStr] = Field(None, description='Client message')
    invalid_properties: Optional[Dict[str, List[StrictStr]]] = Field(
        None, alias='invalidProperties',
        description='Key-value pairs of invalid request properties',
    )


''' type: Optional[StrictStr] = Field(None, description='type')
 title: Optional[StrictStr] = Field(None, description='title')
 status: Optional[int] = Field(None, description='status')
 traceId: Optional[StrictStr] = Field(None, description='traceId')
 errors: Optional[Errors] = Field(None, description='errors')'''
