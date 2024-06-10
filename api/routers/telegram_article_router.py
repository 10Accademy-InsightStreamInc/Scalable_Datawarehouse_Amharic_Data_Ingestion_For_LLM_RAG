
from fastapi import APIRouter, Depends,  HTTPException,  status
from sqlalchemy.orm import Session
from  models.database import get_db as session
import view_model.telegram_article_vm   as telegram_article_vm
from controllers  import telegram_article_controller
from typing import List

router = APIRouter(
    prefix="/telegramArticle",
    tags=["telegram_articles"],
    responses={404: {"description": "Not found"}},
)

 
@router.get("/", response_model=List[telegram_article_vm.TelegramArticleVM])
def get_telegram_data(skip: int = 0, limit: int = 100,db: Session = Depends(session)):
    try:
        db_user = telegram_article_controller.get_data(db,skip, limit)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
       
@router.post("/", response_model=telegram_article_vm.TelegramArticleVM)
def create_telegram_data(data: telegram_article_vm.TelegramArticleCreateVM, db: Session = Depends(session)):
    try:
        db_user = telegram_article_controller.create_data(db, data=data)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/search", response_model=List[telegram_article_vm.TelegramArticleVM])
async def search_telegram_data(search_request: telegram_article_vm.TelegramArticleSearch, db: Session = Depends(session)):
    try:
        query = search_request.query
        result = telegram_article_controller.search_data(db, query)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/filter", response_model=List[telegram_article_vm.TelegramArticleVM])
async def filter_telegram_data(data: telegram_article_vm.TelegramArticleFilterVM, db: Session = Depends(session)):
    try:
        result = telegram_article_controller.filter_data(db, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
