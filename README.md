# Toutiao News

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue%203-Frontend-42b883?logo=vue.js&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis&logoColor=white)
![Status](https://img.shields.io/badge/Status-Learning%20Project-orange)

一个面向移动端新闻资讯场景的全栈练手项目，后端基于 **FastAPI + SQLAlchemy Async + MySQL + Redis**，前端基于 **Vue 3 + Vite + Vant + Pinia**。项目实现了新闻分类、新闻列表、新闻详情、用户注册登录、收藏、历史记录，以及前端 AI 问答页面等完整业务链路。

这个仓库虽然名为后端项目，但实际上已经包含：

- `FastAPI` 后端服务
- `Vue 3` 前端子项目 `xwzx-news`
- `MySQL` 数据存储
- `Redis` 缓存支持

如果你想找一个结构清晰、适合作为 FastAPI 全栈入门或课程练习展示的项目，这个仓库可以直接作为基础模板继续扩展。

## 目录

- [项目亮点](#项目亮点)
- [功能清单](#功能清单)
- [技术栈](#技术栈)
- [系统架构](#系统架构)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [接口概览](#接口概览)
- [统一响应格式](#统一响应格式)
- [数据库设计概览](#数据库设计概览)
- [前端页面概览](#前端页面概览)
- [当前已知问题](#当前已知问题)
- [后续优化建议](#后续优化建议)
- [贡献指南](#贡献指南)
- [License](#license)

## 项目亮点

- 基于 `FastAPI` 构建，天然支持高性能异步接口开发。
- 使用 `SQLAlchemy AsyncSession` 连接 `MySQL`，完成异步 CRUD。
- 使用 `Redis` 对新闻分类和新闻列表进行缓存，减少数据库压力。
- 采用模块化分层设计，按 `routers / crud / models / schemas / utils / config` 拆分职责。
- 提供统一响应结构与全局异常处理，便于前后端联调。
- 前端使用 `Vue 3 + Vite + Vant`，适合移动端资讯类界面开发。
- 包含完整的用户能力：注册、登录、查看资料、修改资料、修改密码。
- 包含完整的内容互动能力：新闻详情、阅读历史、新闻收藏。
- 已集成国际化、状态管理与前端路由，适合作为全栈课程项目继续迭代。

## 功能清单

### 后端能力

- 新闻分类查询
- 新闻分页列表查询
- 新闻详情查询
- 新闻阅读量自增
- 同分类相关新闻推荐
- 用户注册
- 用户登录
- 用户信息查询
- 用户资料更新
- 用户密码修改
- 收藏状态检查
- 添加收藏
- 取消收藏
- 收藏列表查询
- 清空收藏
- 添加历史记录
- 历史记录分页查询
- 删除单条历史记录
- 清空历史记录

### 前端能力

- 首页新闻流
- 分类页
- 新闻详情页
- 登录页
- 注册页
- 我的页面
- 个人信息页
- 设置页
- 收藏页
- 浏览历史页
- AI 问答页
- Pinia 本地状态持久化
- Vue I18n 国际化能力

## 技术栈

### 后端

- Python
- FastAPI
- SQLAlchemy 2.x Async ORM
- aiomysql
- Redis
- Pydantic
- Passlib + bcrypt

### 前端

- Vue 3
- Vite
- Vant
- Pinia
- Vue Router
- Vue I18n
- Axios
- Marked
- DOMPurify

### 数据与基础设施

- MySQL
- Redis

## 系统架构

```mermaid
flowchart LR
    A["Vue 3 Frontend<br/>xwzx-news"] --> B["FastAPI API"]
    B --> C["Redis Cache"]
    B --> D["MySQL Database"]
    B --> E["Auth / Exception / Response Utils"]
    D --> F["news / user / favorite / history tables"]
```

### 后端分层说明

- `routers`：定义 API 路由、请求参数和响应流程。
- `crud`：封装数据库查询和更新逻辑。
- `models`：定义 SQLAlchemy ORM 数据模型。
- `schemas`：定义 Pydantic 数据校验和序列化模型。
- `config`：数据库、缓存等基础配置。
- `utils`：认证、密码处理、统一响应、异常处理等公共能力。
- `cache`：新闻分类和新闻列表缓存封装。

## 项目结构

```text
toutiao_backend/
├─ main.py                    # FastAPI 应用入口
├─ config/
│  ├─ db_conf.py              # MySQL 异步连接配置
│  └─ cache_conf.py           # Redis 配置
├─ routers/
│  ├─ news.py                 # 新闻相关接口
│  ├─ users.py                # 用户相关接口
│  ├─ favorite.py             # 收藏相关接口
│  └─ history.py              # 历史记录相关接口
├─ crud/
│  ├─ news.py
│  ├─ news_cache.py
│  ├─ users.py
│  ├─ favorite.py
│  └─ history.py
├─ models/
│  ├─ news.py                 # 新闻、分类模型
│  ├─ users.py                # 用户、Token 模型
│  ├─ favorite.py             # 收藏模型
│  └─ history.py              # 历史记录模型
├─ schemas/
│  ├─ base.py
│  ├─ users.py
│  ├─ favorite.py
│  └─ history.py
├─ utils/
│  ├─ auth.py
│  ├─ response.py
│  ├─ security.py
│  ├─ exception.py
│  └─ exception_handlers.py
├─ cache/
│  └─ ...
└─ xwzx-news/                 # Vue 3 前端子项目
   ├─ src/
   │  ├─ views/
   │  ├─ router/
   │  ├─ store/
   │  ├─ components/
   │  ├─ i18n/
   │  └─ config/
   ├─ package.json
   └─ vite.config.js
```

## 快速开始

### 1. 环境准备

建议本地准备以下环境：

- Python 3.10+
- Node.js 18+
- MySQL 8.x
- Redis 6.x 或更高版本

### 2. 克隆项目

```bash
git clone https://github.com/jydhs/Toutiao-News.git
cd Toutiao-News
```

### 3. 启动后端

如果你使用虚拟环境，建议先创建并激活：

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

安装后端依赖：

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy aiomysql redis pydantic passlib bcrypt
```

启动后端服务：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

启动成功后可访问：

- Swagger 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc 文档：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- 根路由测试：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 4. 启动前端

进入前端子项目目录：

```bash
cd xwzx-news
```

安装依赖：

```bash
npm install
```

启动开发服务器：

```bash
npm run dev
```

前端默认会通过 `src/config/api.js` 中的 `baseURL` 访问后端接口。

## 配置说明

### 1. MySQL 配置

当前项目在 [config/db_conf.py](E:/python_study/toutiao_backend/config/db_conf.py) 中直接写死了数据库连接：

```python
mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4
```

你需要确保本地：

- 已安装并启动 MySQL
- 存在数据库 `news_app`
- 用户名、密码、端口与本地环境一致

更推荐的做法是后续改为 `.env` 环境变量配置。

### 2. Redis 配置

当前 Redis 配置位于 [config/cache_conf.py](E:/python_study/toutiao_backend/config/cache_conf.py)：

- Host: `localhost`
- Port: `6379`
- DB: `0`

请确保 Redis 已启动，否则新闻分类缓存和新闻列表缓存将无法正常工作。

### 3. 前端接口配置

前端 API 地址位于 [xwzx-news/src/config/api.js](E:/python_study/toutiao_backend/xwzx-news/src/config/api.js)：

```js
baseURL: 'http://127.0.0.1:8000'
```

如果你修改了后端端口或部署地址，需要同步调整这里。

### 4. 认证说明

项目当前通过请求头 `Authorization` 读取登录后的 token。

注意：当前后端实现是直接读取 `Authorization` 的原始值进行校验，并没有真正解析 `Bearer <token>` 格式。因此前后端联调时需要保持一致。

## 接口概览

### 新闻模块

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/news/categories` | 获取新闻分类 |
| GET | `/api/news/list` | 获取新闻分页列表 |
| GET | `/api/news/detail` | 获取新闻详情 |

### 用户模块

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/user/register` | 用户注册 |
| POST | `/api/user/login` | 用户登录 |
| GET | `/api/user/info` | 获取当前用户信息 |
| PUT | `/api/user/update` | 更新用户资料 |
| PUT | `/api/user/password` | 修改密码 |

### 收藏模块

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/favorite/check` | 检查是否已收藏 |
| POST | `/api/favorite/add` | 添加收藏 |
| DELETE | `/api/favorite/remove` | 取消收藏 |
| GET | `/api/favorite/list` | 获取收藏列表 |
| DELETE | `/api/favorite/clear` | 清空收藏 |

### 历史记录模块

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/history/add` | 添加浏览历史 |
| GET | `/api/history/list` | 获取浏览历史 |
| DELETE | `/api/history/delete/{history_id}` | 删除单条历史 |
| DELETE | `/api/history/clear` | 清空历史 |

## 统一响应格式

项目大部分接口采用统一返回结构：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

错误时也会通过全局异常处理器返回统一结构，例如：

```json
{
  "code": 401,
  "message": "未授权或 token 无效",
  "data": null
}
```

## 数据库设计概览

从当前 ORM 模型可以整理出以下核心表：

| 表名 | 说明 |
| --- | --- |
| `news_category` | 新闻分类表 |
| `news` | 新闻内容表 |
| `user` | 用户表 |
| `user_token` | 登录 Token 表 |
| `favorite` | 用户收藏表 |
| `history` | 用户浏览历史表 |

### 关键业务关系

- 一个分类对应多条新闻
- 一个用户可以有多个收藏记录
- 一个用户可以有多条历史记录
- 一个用户对应一个当前有效 token 记录

## 前端页面概览

当前前端路由已包含以下页面：

| 页面 | 路由 |
| --- | --- |
| 首页 | `/home` |
| 登录 | `/login` |
| 注册 | `/register` |
| 新闻详情 | `/news/detail/:id` |
| 分类 | `/category` |
| 收藏 | `/favorite` |
| 浏览历史 | `/history` |
| AI 问答 | `/aichat` |
| 我的 | `/my` |
| 个人信息 | `/profile` |
| 设置 | `/settings` |

## 当前已知问题

这个仓库已经可以作为练手项目使用，但从工程化角度看，当前还有一些明显可优化项：

- 缺少标准的 `requirements.txt` 或 `pyproject.toml`，后端依赖需要手动安装。
- 数据库连接、Redis 地址、前端 API 地址等配置目前写死在源码中。
- 前端配置文件中存在第三方 AI 接口配置，生产环境不应将密钥放在前端源码内。
- 仓库当前包含 `.venv`、`node_modules`、`__pycache__`、`.idea` 等不建议提交到 Git 的内容。
- 认证逻辑使用数据库存储 token，适合教学和练习，但不够标准化，可进一步升级为 JWT。
- `Authorization` 头处理方式与常见 Bearer 规范不完全一致。
- 部分文件存在编码问题，中文注释显示异常。
- 暂未看到自动化测试、CI、Docker 化部署与环境变量方案。

## 后续优化建议

如果你准备继续完善这个项目，建议优先按下面的顺序推进：

1. 增加 `.gitignore`，清理 `.venv`、`node_modules`、缓存文件和 IDE 配置。
2. 增加 `requirements.txt` 或迁移到 `pyproject.toml`。
3. 使用 `.env` 管理数据库、Redis、API 地址、密钥等配置。
4. 将认证方式升级为标准 JWT。
5. 为核心接口补充单元测试和集成测试。
6. 为前后端增加 Docker / Docker Compose 支持。
7. 对新闻列表、详情、收藏、历史模块增加更完整的业务校验。
8. 增加部署说明，完善线上演示与截图。

## 贡献指南

欢迎基于这个项目继续学习和扩展。如果你准备协作开发，建议遵循以下流程：

1. Fork 本仓库
2. 创建功能分支
3. 提交修改并自测
4. 发起 Pull Request

如果你只是把它作为自己的课程项目或作品集项目，也很适合继续补充：

- 项目截图
- 数据库初始化脚本
- 演示视频
- Docker 部署文档
- 接口测试集合

## License

当前仓库暂未看到明确的开源 License 文件。

如果你计划公开发布并允许他人复用，建议补充常见开源协议，例如：

- MIT License
- Apache-2.0

---

如果这个项目对你有帮助，欢迎点个 Star，也欢迎继续完善成一个更完整的全栈资讯平台。
