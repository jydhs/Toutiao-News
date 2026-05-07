from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news_cache, news

#创建API实例
# 路由前缀，用于在URL中标识该路由
# tags：路由标签，用于在文档中分类显示
router = APIRouter(prefix="/api/news", tags=["news"])


#接口实现流程
#1. 模块化路由 ——> API接口规范文档
#2. 定义模型类 ——> 数据库表(数据库设计文档)
#3.在crud文件夹里面创建文件，封装操作数据库的方法
#4.在路由处理函数里面调用crud封装好的方法，响应结果

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db:AsyncSession = Depends(get_db)):
    #先获取数据库里面的新闻分类数据——>先定义模型类——>封装查询数据库的方法
    categories = await news_cache.get_category(db,skip,limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

@router.get("/list")
async def get_news_list(category_id: int = Query(...,alias="categoryId"),
                        page: int = 1,
                        page_size: int=Query(10,alias="pageSize",le=100),
                        db:AsyncSession = Depends(get_db)):
    #处理分页规则——查询新闻列表——计算总量——看是否还有更多数据
    offset=(page-1)*page_size
    news_list = await news_cache.get_news_list(db,category_id,offset,page_size)
    total = await news_cache.get_news_count(db,category_id)
    #判断是否有更多数据
    hasmore = total > offset + len(news_list)
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasmore": hasmore
        }
    }

@router.get("/detail")
async def get_news_detail(news_id: int = Query(...,alias="id"),
                        db:AsyncSession = Depends(get_db)):
    #查询新闻详情
    news_detail = await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    #增加新闻点击量
    views_res = await news.increase_news_views(db,news_id)
    if not views_res:
        raise HTTPException(status_code=404,detail="新闻不存在")

    #查询相关新闻
    related_news = await news.get_related_news(db,news_id,news_detail.category_id)



    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time.isoformat(),
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }