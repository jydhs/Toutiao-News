from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

#数据库URL
ASYNC_DATABASE_URL="mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"

#创建异步数据库引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,#输出SQL日志
    pool_size=10,#连接池大小
    max_overflow=20,#最大溢出连接数
)

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

#依赖项，用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
