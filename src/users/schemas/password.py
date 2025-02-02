from typing import Annotated

from pydantic import BaseModel, Field


class ChangePasswordSchema(BaseModel):
    current_password: Annotated[str, Field(validation_alias="currentPassword")]
    new_password: Annotated[str, Field(validation_alias="newPassword")]
