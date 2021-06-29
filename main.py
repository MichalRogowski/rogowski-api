from fastapi import FastAPI
app = FastAPI()

@app.get("/questions")
async def questions():
    return [
        {
        "name":"test",
        "id":"123"
        }
    ]

@app.post("/questions/{question_id}")
async def post_answer(question_id: str):
    return {"question_id": question_id}
