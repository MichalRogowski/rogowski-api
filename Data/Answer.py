from typing import Optional

from pydantic import BaseModel


class Answer(BaseModel):
    option_key: str
    question_key: str
    value: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "option_key": "2",
                "question_key": "3skohoe398qj",
            }
        }
