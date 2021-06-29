from pydantic import BaseModel


class Option(BaseModel):
    title: str
    key: str
