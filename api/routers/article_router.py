from fastapi import APIRouter, Depends,  HTTPException,  status
from sqlalchemy.orm import Session
from  models.database import get_db as session
from controllers  import article_controller
from typing import List

import view_model.article_vm as article_vm




router = APIRouter(
    prefix="/article",
    tags=["telegram_articles"],
    responses={404: {"description": "Not found"}},
)



@router.get("/", response_model=List[article_vm.ArticleVM])
def get_data(skip: int = 0, limit: int = 100,db: Session = Depends(session)):
    try:
        db_user = article_controller.get_data(db, skip, limit)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/", response_model=article_vm.ArticleVM)
def create_data(data: article_vm.ArticleCreateVM, db: Session = Depends(session)):
    try:
        db_user = article_controller.create_data(db, data=data)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/search", response_model=List[article_vm.ArticleVM])
async def search_data(search_request: article_vm.ArticleSearch, db: Session = Depends(session)):
    try:
        query = search_request.query
        result = article_controller.search_data(db, query)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/filter", response_model=List[article_vm.ArticleVM])
async def filter_data(data: article_vm.ArticleFilterVM, db: Session = Depends(session)):
    try:
        result = article_controller.filter_data(db, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    
    