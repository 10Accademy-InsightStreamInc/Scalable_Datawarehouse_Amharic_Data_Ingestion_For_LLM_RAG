from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import article_router
from routers import telegram_article_router
import uvicorn
from models.database import create_all_tables



app = FastAPI(
        title="Amharic data integration for LLM",
        description="",
        version="1"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Create tables
create_all_tables()

app.include_router(article_router.router)
app.include_router(telegram_article_router.router)


if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
