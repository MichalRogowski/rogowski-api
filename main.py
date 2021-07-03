from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from deta import Deta

from Data.Question import Question
from Data.Answer import Answer
from Domain.Authenticator import Authenticator
from Domain.HandleAnswersUseCase import HandleAnswersUseCase

app = FastAPI()
router = InferringRouter()
deta = Deta()


@cbv(router)
class Router:
    handle_answers_use_case = HandleAnswersUseCase(deta=deta)

    @router.get("/questions")
    async def get_list_of_available_questions(self):
        questions_db = deta.Base("questions")
        return list(questions_db.fetch())[0]

    @router.post(
        "/questions",
        status_code=201,
        dependencies=[Depends(Authenticator.confirm_basic_auth)],
    )
    async def create_question(self, question: Question):
        questions_db = deta.Base("questions")
        return questions_db.put(question.dict())

    @router.delete(
        "/questions/{question_key}",
        status_code=204,
        dependencies=[Depends(Authenticator.confirm_basic_auth)],
    )
    async def delete_question(self, question_key: str):
        db = deta.Base("questions")
        return db.delete(question_key)

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
        except:
            raise HTTPException(
                status_code=404, detail="Question with this key does not exist"
            )

    @router.get("/answers/{question_key}", response_model=List[Answer])
    async def get_answers_for_question(self, question_key: str):
        db = deta.Base("answers")
        return list(db.fetch({"question_key": question_key}))[0]


app.include_router(router)
