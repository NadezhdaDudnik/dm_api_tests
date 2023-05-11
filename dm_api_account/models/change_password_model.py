from pydantic import BaseModel, StrictStr, Field


class ChangePasswordModel(BaseModel):
    login: StrictStr
    token: StrictStr
    oldPassword: StrictStr
    newPassword: StrictStr
