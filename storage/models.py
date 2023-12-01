import datetime

from typing import Any
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, text, update, bindparam
from sqlalchemy import select

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import JSONB

from storage.base import Base, intpk, async_session


class SearchRequest(Base):
    __tablename__ = 'search_request'
    # local_id
    local_id: Mapped[intpk]

    # relation with CHILD
    meta_data: Mapped['SRMetadata'] = relationship(back_populates='search_request')
    params: Mapped['SRParams'] = relationship(back_populates='search_request')
    products: Mapped['SRProduct'] = relationship(back_populates='search_request')

    # fields
    state: Mapped[Optional[int]]
    version: Mapped[Optional[int]]

    # additional fields
    query: Mapped[Optional[str]]
    page: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class SRMetadata(Base):
    __tablename__ = 'sr_metadata'
    # local_id
    local_id: Mapped[intpk]

    # relation to Parent
    search_request_id = mapped_column(ForeignKey('search_request.local_id'))
    search_request: Mapped['SearchRequest'] = relationship(back_populates='meta_data')

    # fields
    name: Mapped[Optional[str]]
    catalog_type: Mapped[Optional[str]]
    catalog_value: Mapped[Optional[str]]
    normquery: Mapped[Optional[str]]
    ContextMetadata: Mapped[dict[str, Any]] = mapped_column(type_=JSONB)


class SRParams(Base):
    __tablename__ = 'sr_params'
    # local_id
    local_id: Mapped[intpk]
    # relation to PARENT
    search_request_id = mapped_column(ForeignKey('search_request.local_id'))
    search_request = relationship('SearchRequest', back_populates='params')

    version: Mapped[Optional[int]]
    curr: Mapped[Optional[str]]
    spp: Mapped[Optional[int]]
    dest: Mapped[Optional[int]]
    payloadVersion: Mapped[Optional[int]]


class SRProduct(Base):
    __tablename__ = 'sr_product'
    # local id
    local_id: Mapped[intpk]

    # relation to PARENT
    search_request_id = mapped_column(ForeignKey('search_request.local_id'))
    search_request = relationship('SearchRequest', back_populates='products')

    # relations with a CHILD's
    colors: Mapped[List['SRProductColor']] = relationship(back_populates='product')
    sizes: Mapped[List['SRProductSize']] = relationship(back_populates='product')
    log: Mapped[List['SRProductLog']] = relationship(back_populates='product')

    # fields
    time1: Mapped[Optional[int]]
    time2: Mapped[Optional[int]]
    dist: Mapped[Optional[int]]
    id: Mapped[Optional[int]]
    root: Mapped[Optional[int]]
    kindId: Mapped[Optional[int]]
    subjectId: Mapped[Optional[int]]
    subjectParentId: Mapped[Optional[int]]
    name: Mapped[Optional[str]]
    brand: Mapped[Optional[str]]
    brandId: Mapped[Optional[int]]
    siteBrandId: Mapped[Optional[int]]
    supplier: Mapped[Optional[str]]
    supplierId: Mapped[Optional[int]]
    sale: Mapped[Optional[int]]
    priceU: Mapped[Optional[int]]
    salePriceU: Mapped[Optional[int]]
    logisticsCost: Mapped[Optional[int]]
    saleConditions: Mapped[Optional[int]]
    returnCost: Mapped[Optional[int]]
    pics: Mapped[Optional[int]]
    rating: Mapped[Optional[int]]
    reviewRating: Mapped[Optional[int]]
    feedbacks: Mapped[Optional[int]]
    panelPromoId: Mapped[Optional[int]]
    promoTextCard: Mapped[Optional[str]]
    promoTextCat: Mapped[Optional[str]]
    volume: Mapped[Optional[int]]
    viewFlags: Mapped[Optional[int]]
    isNew: Mapped[bool] = mapped_column(nullable=True)
    diffPrice: Mapped[bool] = mapped_column(nullable=True)

    processed_at: Mapped[Optional[datetime.datetime]]

    @staticmethod
    async def get_ids_list():
        async with async_session() as session:
            query = (
                select(SRProduct.local_id)
            )
            res = await session.execute(query)
            ids_list = res.scalars().all()
            return ids_list

    @staticmethod
    async def bulk_update_processed_time(products_id: list[int]) -> set:
        """
        :param products_id: list[id]  products for update
        :return: set[id] - non-existing products
        """
        update_stmt = (
            update(SRProduct)
            .where(SRProduct.local_id.in_(products_id))
            .values(processed_at=datetime.datetime.utcnow())
        )

        async with async_session() as session:
            result = await session.execute(
                update_stmt.returning(SRProduct.local_id)
            )
            await session.commit()

        updated_rows = result.scalars().fetchall()
        errors = set(products_id) - set(updated_rows)

        return errors


class SRProductLog(Base):
    __tablename__ = 'sr_product_log'

    # local id
    local_id: Mapped[intpk]

    # relation to product
    product_id: Mapped[int] = mapped_column(ForeignKey('sr_product.local_id'))
    product: Mapped['SRProduct'] = relationship(back_populates='log')

    cpm: Mapped[Optional[int]]
    promotion: Mapped[Optional[int]]
    promoPosition: Mapped[Optional[int]]
    position: Mapped[Optional[int]]
    advertId: Mapped[Optional[int]]


class SRProductColor(Base):
    __tablename__ = 'sr_product_color'
    # local id
    local_id: Mapped[intpk]

    # relation with product
    product_id: Mapped[int] = mapped_column(ForeignKey('sr_product.local_id'))
    product: Mapped['SRProduct'] = relationship(back_populates='colors')

    # fields
    id: Mapped[Optional[int]]
    name: Mapped[Optional[str]]


class SRProductSize(Base):
    __tablename__ = 'sr_product_size'

    # local id
    local_id: Mapped[intpk]

    # relation to product
    product_id: Mapped[int] = mapped_column(ForeignKey('sr_product.local_id'))
    product: Mapped['SRProduct'] = relationship(back_populates='sizes')

    # fields
    name: Mapped[Optional[str]]
    origName: Mapped[Optional[str]]
    rank: Mapped[Optional[int]]
    optionId: Mapped[Optional[int]]
    returnCost: Mapped[Optional[int]]
    wh: Mapped[Optional[int]]
    sign: Mapped[Optional[str]]
    payload: Mapped[Optional[str]]
