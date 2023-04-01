from typing import List
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination, paginate, Page, LimitOffsetPage
from db import SessionLocal, ProductModel
from schemas import ProductOutput


app = FastAPI()

@app.get('/products', response_model=List[ProductOutput])
def get_products():
    fake_products = [
        ProductOutput(name=f'Flamengo {n}', price=n * .1, id=n)
        for n in range(100)
    ]

    return fake_products


@app.get('/products/paginate/default', response_model=Page[ProductOutput])
@app.get('/products/paginate/limit-offset', response_model=LimitOffsetPage[ProductOutput])
def get_products():
    fake_products = [
        ProductOutput(name=f'Flamengo {n}', price=n * .1, id=n)
        for n in range(100)
    ]

    return paginate(fake_products)

add_pagination(app)
