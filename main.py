from typing import Union
from fastapi import FastAPI
from basic_code.scripts.basic_code_func import basic_function
from pydantic import BaseModel
from fastapi.responses import FileResponse


class Item(BaseModel):
    type: Union[str, None] = None
    name: str
    crs: Union[dict, None] = None
    features: list


app = FastAPI()


@app.post("/get_ndvi_img/")
async def get_body(item: Item):
    result = basic_function(item.features[0]['geometry'])
    return FileResponse(result)


@app.get("/")
async def root():
    return {'message': 'hello'}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
