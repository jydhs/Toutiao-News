from sqlalchemy import Select, func, Update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


async def get_category(db: AsyncSession,skip: int = 0, limit: int = 100):
    stmt = Select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db: AsyncSession,category_id: int,skip: int = 0, limit: int = 10):
    #查询新闻列表
    #根据分类ID查询新闻列表
    stmt = Select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

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
