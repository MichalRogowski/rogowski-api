from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from deta import Deta

import View.QuestionsRouter
from Data.Answer import Answer
from Domain.Authenticator import Authenticator
from Domain.HandleAnswersUseCase import HandleAnswersUseCase

app = FastAPI()


def get_deta() -> Deta:
    return Deta()


router = InferringRouter(dependencies=[Depends(get_deta)])


def get_answers_use_case() -> HandleAnswersUseCase:
    return HandleAnswersUseCase(deta=get_deta)


@cbv(router)
class Router:
    @router.get(
        "/answers",
        response_model=List[Answer],
        dependencies=[Depends(Authenticator.confirm_basic_auth)],
    )
    async def get_list_of_answers(self):
        db = deta.Base("answers")
        return list(db.fetch())[0]

    @router.post("/answers", status_code=201)
    async def post_answer(self, answer: Answer):
        try:
            return self.handle_answers_use_case.add_answer(answer=answer)
        except ValueError:
            raise HTTPException(
                status_code=404, detail="Question with this key does not exist"
            )

    @router.get("/answers/{question_key}", response_model=List[Answer])
    async def get_answers_for_question(self, question_key: str):
        self.handle_answers_use_case.get_answers_for_key(question_key=question_key)


app.include_router(router)
app.include_router(View.QuestionsRouter.get_questions_router())
