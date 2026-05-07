from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import news, users, favorite, history
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
#注册异常处理器
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#允许的源，开发阶段允许所有，生产环境需要指定
    allow_credentials=True,#是否允许携带凭证，如cookies、Authorization头等
    allow_methods=["*"],#允许的请求方法
    allow_headers=["*"],#允许的请求头
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

#挂载路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
