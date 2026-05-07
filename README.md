# Toutiao-News

一个以 **FastAPI 后端接口开发** 为核心的练手项目。

这个仓库的重点是后端服务本身，包括：

- FastAPI 路由组织
- 用户、新闻、收藏、历史记录等接口
- MySQL 异步数据库访问
- Redis 缓存
- FastAPI 自动生成接口文档

仓库中虽然包含 `xwzx-news` 前端目录，但它更像是一个用于联调和展示接口效果的载体，不是本项目的核心重点。

## 目录

- [项目重点](#项目重点)
- [快速启动](#快速启动)
- [FastAPI 接口文档](#fastapi-接口文档)
- [运行前准备](#运行前准备)
- [项目结构](#项目结构)
- [主要接口](#主要接口)
- [配置位置](#配置位置)
- [说明](#说明)

## 项目重点

这个项目最值得关注的是后端部分：

- 使用 `main.py` 作为 FastAPI 启动入口
- 使用 `uvicorn main:app --reload` 启动开发服务
- 自动生成 Swagger 和 ReDoc 接口文档
- 通过模块化目录拆分 `routers / crud / models / schemas / utils / config`

如果你是为了学习 FastAPI 项目怎么落地，这个仓库主要看后端目录即可。

## 快速启动

这是 README 里最重要的部分。

### 1. 启动后端

先进入项目根目录，也就是 `main.py` 所在目录：

```bash
cd E:\python_study\toutiao_backend
```

然后执行：

```bash
uvicorn main:app --reload
```

这就是本项目后端的核心启动方式。

启动成功后，默认访问地址是：

- 后端首页：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- FastAPI Swagger 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- FastAPI ReDoc 文档：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 2. 启动前端

前端不是项目重点，但如果你需要联调页面，仍然可以启动。

需要注意的是：

- 要进入前端目录再开终端
- 在 `xwzx-news` 文件夹里执行 `npm run dev`

步骤如下：

```bash
cd E:\python_study\toutiao_backend\xwzx-news
npm run dev
```

如果你平时在 PyCharm 里操作，更直白一点就是：

1. 打开 `xwzx-news` 目录
2. 在这个前端文件夹里打开终端
3. 执行 `npm run dev`

前端启动的意义主要是作为接口调用页面，用来配合后端联调。

## FastAPI 接口文档

本项目使用的是 FastAPI，自带自动接口文档，这一点非常适合学习和调试。

后端启动后可以直接打开：

- Swagger UI：`http://127.0.0.1:8000/docs`
- ReDoc：`http://127.0.0.1:8000/redoc`

推荐优先使用 Swagger UI，也就是 `/docs`，因为它可以：

- 直接查看所有接口
- 查看请求参数和返回结构
- 在线测试接口
- 调试登录、新闻、收藏、历史记录等功能

如果你只是想验证后端有没有跑起来，打开 `/docs` 基本就是最快的方法。

## 运行前准备

在启动前，建议先准备这些环境：

- Python 3.10+
- Node.js 18+
- MySQL
- Redis

### 后端依赖

如果本地还没装依赖，可以手动安装：

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy aiomysql redis pydantic passlib bcrypt
```

### 数据库

当前项目数据库连接写在 [db_conf.py](E:/python_study/toutiao_backend/config/db_conf.py)：

```python
mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4
```

也就是说你本地需要至少满足：

- MySQL 已启动
- 存在 `news_app` 数据库
- 用户名、密码、端口与代码配置一致

### Redis

Redis 配置在 [cache_conf.py](E:/python_study/toutiao_backend/config/cache_conf.py)：

- `host = localhost`
- `port = 6379`
- `db = 0`

如果 Redis 没启动，新闻缓存相关能力会受影响。

## 项目结构

这里重点只看后端主结构：

```text
toutiao_backend/
├─ main.py
├─ config/
│  ├─ db_conf.py
│  └─ cache_conf.py
├─ routers/
│  ├─ news.py
│  ├─ users.py
│  ├─ favorite.py
│  └─ history.py
├─ crud/
├─ models/
├─ schemas/
├─ utils/
├─ cache/
└─ xwzx-news/
```

可以这样理解：

- `main.py`：项目启动入口
- `routers`：接口路由定义
- `crud`：数据库操作逻辑
- `models`：数据库模型
- `schemas`：请求和响应的数据模型
- `utils`：认证、异常、响应封装
- `xwzx-news`：前端联调用页面

## 主要接口

### 新闻

- `GET /api/news/categories`
- `GET /api/news/list`
- `GET /api/news/detail`

### 用户

- `POST /api/user/register`
- `POST /api/user/login`
- `GET /api/user/info`
- `PUT /api/user/update`
- `PUT /api/user/password`

### 收藏

- `GET /api/favorite/check`
- `POST /api/favorite/add`
- `DELETE /api/favorite/remove`
- `GET /api/favorite/list`
- `DELETE /api/favorite/clear`

### 历史记录

- `POST /api/history/add`
- `GET /api/history/list`
- `DELETE /api/history/delete/{history_id}`
- `DELETE /api/history/clear`

更完整的参数和调试方式，请直接看 FastAPI 自动文档：

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 配置位置

几个最常用的地方如下：

- 后端启动入口：[main.py](E:/python_study/toutiao_backend/main.py)
- 数据库配置：[db_conf.py](E:/python_study/toutiao_backend/config/db_conf.py)
- Redis 配置：[cache_conf.py](E:/python_study/toutiao_backend/config/cache_conf.py)
- 前端接口地址：[api.js](E:/python_study/toutiao_backend/xwzx-news/src/config/api.js)

## 说明

当前仓库更适合作为学习型项目，而不是可直接上线的生产项目。现在还存在这些典型情况：

- 配置是直接写在代码里的
- 仓库里包含前端依赖和虚拟环境痕迹
- 缺少标准依赖文件和部署说明

但如果你的目标是：

- 学习 FastAPI 项目结构
- 学习 `uvicorn main:app --reload` 的本地开发方式
- 学习怎么用 `/docs` 快速调接口
- 学习前后端联调的最小闭环

那这个项目已经很适合作为练手样例。
