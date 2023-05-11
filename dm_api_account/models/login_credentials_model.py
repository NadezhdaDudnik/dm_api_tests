
from pydantic import BaseModel, StrictStr, StrictBool, Field


class LoginCredentialsModel(BaseModel):
    login: StrictStr
    password: StrictStr
    rememberMe: StrictBool
