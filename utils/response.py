from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
def success_response(message: str = "success", data=None):
    #把fastapi，padantic，ORM对象都能转换为json格式
    content={
        "code": 200,
        "message": message,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))

