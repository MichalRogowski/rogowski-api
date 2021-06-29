from typing import List

from fastapi import FastAPI
from deta import Deta

from Data.Question import Question
from Data.Answer import Answer

app = FastAPI()
deta = Deta()


@app.get("/questions")
async def get_list_of_available_questions():
    questions_db = deta.Base("questions")
    return list(questions_db.fetch())[0]


@app.post("/questions", status_code=201)
async def create_question(question: Question):
    questions_db = deta.Base("questions")
    return questions_db.put(question.dict())


@app.get("/answers", response_model=List[Answer])
async def get_list_of_answers():
    db = deta.Base("answers")
    return list(db.fetch())[0]


@app.post("/answers", status_code=201)
async def post_answer(answer: Answer):
    db = deta.Base("answers")
    return db.put(answer.dict())
