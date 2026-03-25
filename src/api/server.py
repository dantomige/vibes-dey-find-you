from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

class CreateUserRequests(BaseModel):
    name: str
    email: EmailStr

class RecommendRequest(BaseModel):
    prompt: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "The vibes dey find you."}

@app.post("/users")
def create_user(request: CreateUserRequests):
    pass

@app.post("/recommend")
def recommend(request: RecommendRequest):
    pass
