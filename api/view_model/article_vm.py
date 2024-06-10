# from typing import Optional
# from pydantic import BaseModel


# class ArticleBaseVM(BaseModel):
#     image_url : str 
#     title : str
#     article_url : str
#     highlight : str
#     time_publish : str
#     category : str
#     date_published : str
#     publisher_name : str
#     detail_content : str
   
   
# class ArticleCreateVM(ArticleBaseVM):
#     pass

# class ArticleVM(ArticleBaseVM):
#     id: int
   

#     class Config:
#         orm_mode = True



# class ArticleSearch(BaseModel):
#     query: str
    

# class ArticleFilterVM(BaseModel):
#     id:int | None = None
#     image_url : str | None = None
#     title : str | None = None
#     article_url : str | None = None
#     highlight : str | None = None
#     time_publish : str | None = None
#     category : str | None = None
#     date_published : str | None = None
#     publisher_name : str | None = None
#     detail_content : str | None = None
   
from typing import Optional
from pydantic import BaseModel


class ArticleBaseVM(BaseModel):
    image_url : str 
    title : str
    article_url : str
    highlight : str
    time_publish : str
    category : str
    date_published : str
    publisher_name : str
    detail_content : str
   
   
class ArticleCreateVM(ArticleBaseVM):
    pass

class ArticleVM(ArticleBaseVM):
    id: int
   

    class Config:
        orm_mode = True



class ArticleSearch(BaseModel):
    query: str
    

class ArticleFilterVM(BaseModel):
    id: Optional[int] = None
    image_url : Optional[str]
    title : Optional[str]
    article_url : Optional[str]
    highlight : Optional[str]
    time_publish : Optional[str]
    category : Optional[str]
    date_published : Optional[str]
    publisher_name : Optional[str]
    detail_content : Optional[str]