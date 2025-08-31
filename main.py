import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing_extensions import Annotated

from beanie import Document, Indexed, init_beanie

from fastapi import FastAPI, Depends

app = FastAPI()

class Product(Document):
    name: str
    age: int

class addProduct(BaseModel):
    name: str
    age: int

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.products, document_models=[Product])

async def example():
    name = await Product.find_one(Product.name == 'Pavel')
    return name.name


@app.post("/")
async def set_root(product: Annotated[addProduct, Depends()]):
    newObj = Product(**product.dict())
    await newObj.insert()
    return newObj

@app.get("/")
async def read_root():
    msg = await example()
    return {"name": msg}
#if __name__ == "__main__":
    