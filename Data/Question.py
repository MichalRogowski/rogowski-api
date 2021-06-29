from typing import List
from pydantic import BaseModel
from Data.Option import Option


class Question(BaseModel):
    title: str
    description: str
    options: List[Option] = []

    class Config:
        schema_extra = {
            "example": {
                "title": "How did you found out about my CV app?",
                "description": "How have you found this app?",
                "options": [
                    {"key": "1", "title": "Article"},
                    {"key": "2", "title": "LinkedIn"},
                    {"key": "3", "title": "Twitter"},
                    {"key": "4", "title": "Other"},
                ],
            }
        }
