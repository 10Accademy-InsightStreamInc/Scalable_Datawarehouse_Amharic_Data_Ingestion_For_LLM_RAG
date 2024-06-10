from fastapi import HTTPException, status
from sqlalchemy import String,  inspect, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.telegram_article import TelegramArticle
from view_model.telegram_article_vm import TelegramArticleCreateVM, TelegramArticleFilterVM 
from typing import List


def create_data(db: Session, data: TelegramArticleCreateVM):
    try:
        db_data = TelegramArticle(
            channel=data.channel,
            message=data.message,
            date=data.date
        )
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_data(db: Session,skip: int = 0, limit: int = 100) -> List[TelegramArticle]:
    try:
        return db.query(TelegramArticle).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def search_data(db: Session, query: str) -> List[TelegramArticle]:
    try:
        search_term = f"%{query}%"
        columns = [column.name for column in inspect(TelegramArticle).columns]
        filters = []
        for column in columns:
            col_attr = getattr(TelegramArticle, column)
            if isinstance(col_attr.type, String):
                filters.append(col_attr.like(search_term))
        results = db.query(TelegramArticle).filter(or_(*filters)).all()
        return results
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def filter_data(db: Session, filter_params: TelegramArticleFilterVM) -> List[TelegramArticle]:
    try:
        query = db.query(TelegramArticle)
        if filter_params.id is not None:
            query = query.filter(TelegramArticle.id == filter_params.id)
        if filter_params.channel is not None:
            query = query.filter(TelegramArticle.channel == filter_params.channel)
        if filter_params.message is not None:
            query = query.filter(TelegramArticle.message == filter_params.message)
        if filter_params.date is not None:
            query = query.filter(TelegramArticle.date == filter_params.date)
        return query.all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))