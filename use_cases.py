from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy.orm import Session
from db import ProductModel


def get_products_use_case(db_session: Session, size: int = 50, page: int = 1):
    product_query = db_session.query(ProductModel) # SELECT * FROM products;
    params = Params(page=page, size=size)
    return paginate(product_query, params=params)

