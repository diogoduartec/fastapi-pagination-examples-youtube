from typing import List
from fastapi import FastAPI, Depends, Query
from fastapi_pagination import add_pagination, paginate, Page, LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from sqlalchemy.orm import Session
from db import SessionLocal, ProductModel
from use_cases import get_products_use_case
from schemas import ProductOutput


app = FastAPI()


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/products', response_model=List[ProductOutput])
def get_products():
    fake_products = [
        ProductOutput(name=f'Flamengo {n}', price=n * .1, id=n)
        for n in range(100)
    ]

    return fake_products


@app.get('/products/paginate/default', response_model=Page[ProductOutput])
@app.get('/products/paginate/limit-offset', response_model=LimitOffsetPage[ProductOutput])
def get_products_paginate():
    fake_products = [
        ProductOutput(name=f'Flamengo {n}', price=n * .1, id=n)
        for n in range(100)
    ]

    return paginate(fake_products)


@app.get('/db/products/paginate/default', response_model=Page[ProductOutput])
@app.get('/db/products/paginate/limit-offset', response_model=LimitOffsetPage[ProductOutput])
def get_products_paginate_db(db_session: Session = Depends(get_db_session)):
    product_query = db_session.query(ProductModel) # SELECT * FROM products;
    return sqlalchemy_paginate(product_query)


@app.get('/db/products/paginate/default/custom', response_model=Page[ProductOutput])
def get_products_paginate_db(
    db_session: Session = Depends(get_db_session),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100)
):
    return get_products_use_case(db_session=db_session, page=page, size=size)

# add_pagination(app)
