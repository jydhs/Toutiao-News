from typing import Optional

from pydantic import BaseModel, ConfigDict, Field



class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True,
    )



#data数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_Info: UserInfoResponse=Field(...,alias="userInfo")

    #模型类配置
    model_config=ConfigDict(
        populate_by_name=True,
        from_attributes=True,#和model_validate()方法配合使用，确保模型字段值与数据库字段值保持一致
        #支持同时使用「字段原名」和「别名 (alias)」 给模型赋值 / 解析数据
    )


#更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(...,min_length=6, alias="oldPassword", description="旧密码")
    new_password: str = Field(...,min_length=6,  alias="newPassword", description="新密码")
