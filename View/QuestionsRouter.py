from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from Data.Question import Question
from Domain.Authenticator import Authenticator
from main import get_deta


router = InferringRouter(dependencies=[Depends(get_deta)])


def get_questions_router() -> InferringRouter:
    return router


@cbv(router)
class QuestionsRouter:
    @router.get("/questions")
    async def get_list_of_available_questions(self):
        questions_db = self.deta.Base("questions")
        return list(questions_db.fetch())[0]

    @router.post(
        "/questions",
        status_code=201,
        dependencies=[Depends(Authenticator.confirm_basic_auth)],
    )
    async def create_question(self, question: Question):
        questions_db = self.deta.Base("questions")
        return questions_db.put(question.dict())

    @router.delete(
        "/questions/{question_key}",
        status_code=204,
        dependencies=[Depends(Authenticator.confirm_basic_auth)],
    )
    async def delete_question(self, question_key: str):
        db = self.deta.Base("questions")
        return db.delete(question_key)
