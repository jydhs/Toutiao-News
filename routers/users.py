from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from crud import users
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])
@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    #注册逻辑
    #检查用户名是否存在，存在则返回错误，不存在则注册用户，生成token，返回成功信息
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户名已存在")
    #创建用户
    user=await users.create_user(db,user_data)
    #生成token
    token=await users.create_token(db,user.id)
    return success_response(message="注册成功",
                            data=UserAuthResponse(token=token,
                            user_Info=UserInfoResponse.model_validate(
                                user)))
    #user就是ORM对象，所以必须from_attributes=True
    # return {"code": 200,
    #         "message": "注册成功",
    #         "data": {
    #             "token": token,
    #             "userInfo":{
    #                 "id": user.id,
    #                 "username": user.username,
    #                 "bio": user.bio,
    #                 "avatar": user.avatar,
    #             }
    #         }
    # }
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    #登录逻辑：验证用户是否存在——验证密码——生成token——返回成功信息
    user=await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    #生成token
    token=await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token,
                            user_Info=UserInfoResponse.model_validate(
                                user))
    return success_response(message="登录成功",
                            data=response_data)


#查Token查用户封装crud功能整合成一个工具函数路由导入使用:依赖注入
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",
                            data=UserInfoResponse.model_validate(user))


#修改用户信息：验证Token——更新用户信息(put提交，请求体参数，定义pydantic模型类)——返回成功信息
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    #更新用户信息
    user = await users.update_user(db,user.username,user_data)
    return success_response(message="更新用户信息成功",
                            data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(password_data: UserChangePasswordRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    #更新密码
    res_change_pwd = await users.change_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="修改密码失败")
    return success_response(message="修改密码成功")
