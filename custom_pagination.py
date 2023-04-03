from typing import Any, Sequence, Generic, TypeVar, Optional
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.utils import verify_params
from pydantic import BaseModel
from fastapi import Query
from sqlalchemy.orm import Query as SQLAlchemyQuery

T = TypeVar("T")


class CustomParams(BaseModel, AbstractParams):
    current_page: int = Query(1, ge=1)
    items_per_page: int = Query(10, ge=1, le=100)

    def to_raw_params(self):
        return RawParams(
            limit=self.items_per_page,
            offset=self.items_per_page * (self.current_page - 1)
        )


class CustomPage(AbstractPage[T], Generic[T]):
    items: Sequence[T]
    current_page: int
    items_per_page: int

    __params_type__ = CustomParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: CustomParams,
        **kwargs: Any
    ):
        return cls(
            items=items,
            current_page=params.current_page,
            items_per_page=params.current_page,
            **kwargs
        )


def paginate_query(query: T, params: AbstractParams) -> T:
    raw_params = params.to_raw_params().as_limit_offset()
    return query.limit(raw_params.limit + 1).offset(raw_params.offset + 1)


def custom_sqlalchemy_paginate(
    query: SQLAlchemyQuery[Any],
    params: Optional[AbstractParams] = None,
    **kwargs: Any
) -> Any:
    params, _ = verify_params(params, "limit-offset")

    items = paginate_query(query, params).all()

    return CustomPage.create(
        items=items,
        params=params,
        **kwargs
    )
