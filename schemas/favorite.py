from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    isFavorite: bool = Field(...,alias="isFavorite")


class FavoriteAddRequest(BaseModel):
    news_Id: int = Field(...,alias="newsId")




class FavoriteNewsItemResponse(NewsItemBase):
    favorite_time: datetime = Field(alias="favoriteTime")
    favorite_id: int = Field(alias="favoriteId")

    model_config = ConfigDict(
            populate_by_name=True,
            from_attributes=True
    )


   #收藏列表接口响应的模型类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
