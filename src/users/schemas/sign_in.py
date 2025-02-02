from pydantic import BaseModel


class SignInSchema(BaseModel):
    username: str
    password: str
