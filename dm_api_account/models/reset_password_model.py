from pydantic import BaseModel, StrictStr, Field


class ResetPasswordModel(BaseModel):
    login: StrictStr
    email: StrictStr
