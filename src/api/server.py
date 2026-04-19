import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from src.db.session import get_db
import src.api.requests as requests
import src.api.responses as responses
from src.db.crud.core import SongRepository
from src.db.crud.vector import VectorDBRepository
from src.ml.embedding import EmbeddingModel
from src.services.recommender import RecommenderService
from src.services.model_management_service import ModelManagementService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to manage startup and shutdown events."""
    # Perform any necessary startup tasks here
    model_management_service = ModelManagementService()
    app.state.model_management_service = model_management_service
    app.state.current_model = model_management_service.get_current_model()
    app.state.embedding_model = EmbeddingModel()
    app.state.vector_db_repository = VectorDBRepository()
    yield
    # Perform any necessary shutdown tasks here


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_recommender_service(
    request: Request, db: Session = Depends(get_db)
) -> RecommenderService:
    return RecommenderService(
        model=request.app.state.current_model,
        song_repository=SongRepository(db=db),
        vector_db_repository=request.app.state.vector_db_repository,
        embedding_model=request.app.state.embedding_model,
    )


@app.get("/")
def root():
    return {"message": "The vibes dey find you."}


@app.post("/recommend")
def recommend(
    request: requests.RecommendRequest,
    recommender_service: RecommenderService = Depends(get_recommender_service),
) -> responses.RecommendResponse:

    query = request.query
    num_songs = request.num_songs


    recommendations = recommender_service.recommend_songs(query, num_songs)
    song_responses = [
        responses.SongResponse(
            id=song.id,
            title=song.title,
            artists=song.artists,
            score=score,
        )
        for song, score in recommendations
    ]
    return responses.RecommendResponse(query=query, songs=song_responses)


if __name__ == "__main__":

    print("Running server on http://localhost:8000")

    uvicorn.run("src.api.server:app", reload=True)