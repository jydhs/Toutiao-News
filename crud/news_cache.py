from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, func, Update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cache_categories, get_cached_news_list, set_cache_news_list
from models.news import Category, News
from schemas.base import NewsItemBase


async def get_category(db: AsyncSession,skip: int = 0, limit: int = 100):
    #先尝试从缓存中获取分类列表
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    #如果缓存中没有分类列表，从数据库中查询
    stmt = Select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()# ORM对象

    #写入缓存
    if categories:
        #将ORM对象转换为字典等json能认识的格式
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    #返回数据
    return categories

async def get_news_list(db: AsyncSession,category_id: int,skip: int = 0, limit: int = 10):
    #查询新闻列表
    #根据分类ID查询新闻列表
    #先尝试从缓存中获取新闻列表
    page=skip//limit+1
    cached_list = await get_cached_news_list(category_id, page, limit)
    if cached_list:
        return [News(**item) for item in cached_list]#将JSON转换为ORM对象

    #如果缓存中没有新闻列表，从数据库中查询
    stmt = Select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    #写入缓存
    if news_list:
        # 将ORM对象转换为字典等json能认识的格式
        # 将ORM转成pydantic模型,再转换为字典
        #by_alias= False 表示使用字段名，而不是别名，默认是True,因为redis是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)

    return news_list

async def get_news_count(db: AsyncSession,category_id: int):
    stmt = Select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_news_detail(db: AsyncSession,news_id: int):
    stmt = Select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db: AsyncSession,news_id: int):
    stmt = Update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_related_news(db: AsyncSession,news_id: int,category_id: int,limit: int = 5):
    stmt = Select(News).where(
    News.id != news_id,News.category_id == category_id
    ).order_by(News.views.desc(),News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news=result.scalars().all()
    return [{"id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time.isoformat(),
            "categoryId": news_detail.category_id,
            "views": news_detail.views
             } for news_detail in related_news ]
