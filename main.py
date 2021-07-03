from typing import List

from fastapi import Depends, FastAPI
from deta import App
from deta import Deta

from Data.Question import Question
from Data.Answer import Answer
from Domain.Authenticator import Authenticator

app = App(FastAPI())
deta = Deta()


@app.get("/questions")
async def get_list_of_available_questions():
    questions_db = deta.Base("questions")
    return list(questions_db.fetch())[0]


@app.post(
    "/questions",
    status_code=201,
    dependencies=[Depends(Authenticator.confirm_basic_auth)],
)
async def create_question(question: Question):
    questions_db = deta.Base("questions")
    return questions_db.put(question.dict())


@app.delete(
    "/questions/{question_key}",
    status_code=204,
    dependencies=[Depends(Authenticator.confirm_basic_auth)],
)
async def delete_question(question_key: str):
    db = deta.Base("questions")
    return db.delete(question_key)


@app.get(
    "/answers",
    response_model=List[Answer],
    dependencies=[Depends(Authenticator.confirm_basic_auth)],
)
async def get_list_of_answers():
    db = deta.Base("answers")
    return list(db.fetch())[0]


@app.post("/answers", status_code=201)
async def post_answer(answer: Answer):
    db = deta.Base("answers")
    return db.put(answer.dict())


@app.get("/answers/{question_key}", response_model=List[Answer])
async def get_answers_for_question(question_key: str):
    db = deta.Base("answers")
    return list(db.fetch({"question_key": question_key}))[0]
