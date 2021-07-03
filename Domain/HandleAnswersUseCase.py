from dataclasses import dataclass
from typing import List

from deta import Deta
from fastapi import FastAPI

from Data.Answer import Answer
from Data.Question import Question


@dataclass
class HandleAnswersUseCase:
    deta: Deta

    def get_questions(self) -> List[Question]:
        db = self.deta.Base("questions")
        return list(db.fetch())[0]

    def add_answer(self, answer: Answer):
        questions = self._get_questions_for_key(answer.question_key)
        if len(questions) <= 0:
            raise ValueError(f"Question Key {answer.question_key} does not exist")
        db = self.deta.Base("answers")
        return db.put(answer.dict())

    def _get_questions_for_key(self, question_key):
        db = self.deta.Base("questions")
        return list(db.fetch({"key": question_key}))[0]
