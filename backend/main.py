from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "TaskSight AI Backend Running"}


@app.get("/about")
def about():
    return {
        "project": "TaskSight AI",
        "purpose": "Vision-Language Model Experimentation Platform",
        "status": "Backend Working Successfully"
    }

@app.get("/greet")
def greet(name: str):
    return {"message": f"Hello {name}, welcome to TaskSight AI"}

class UserInput(BaseModel):
    name: str
    role: str


@app.post("/user")
def create_user(user: UserInput):
    return {
        "message": f"{user.name} is working as {user.role}"
    }