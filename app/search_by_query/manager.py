import time
from logging import getLogger

from typing import Mapping
from typing import Any
from typing import List

from storage.base import async_session
from storage.models import SearchRequest
from storage.models import SRMetadata
from storage.models import SRParams
from storage.models import SRProduct
from storage.models import SRProductColor
from storage.models import SRProductSize
from storage.models import SRProductLog

logger = getLogger('app.manager')


async def save_parsed_data(data: Mapping[str, Any]) -> None:
    start_time = time.time()

    meta_data = data['metadata']
    params = data['params']
    products = data['data']['products']

    async with async_session() as session:
        sr = SearchRequest()
        sr.state = data.get('state')
        sr.version = data.get('version')
        sr.query = data.get('query')
        sr.page = data.get('page')

        meta_data = SRMetadata(**meta_data)
        meta_data.search_request = sr

        params = SRParams(**params)
        params.search_request = sr
        session.add_all([sr, meta_data, params])
        await session.commit()
    await insert_sr_products(sr, products)
    end_time = time.time()
    elapsed_time = end_time - start_time

    logger.info('Saved in {:.2f} seconds'.format(elapsed_time))


async def insert_sr_products(sr, products):
    to_commit = []
    for product in products:
        colors_list: List[Mapping[str, Any]] = product.pop('colors')
        sizes_list: List[Mapping[str, Any]] = product.pop('sizes')
        log: Mapping[str, Any] = product.pop('log')

        sr_product: SRProduct = SRProduct(**product)
        sr_product.search_request = sr

        sr_product_log: SRProductLog = SRProductLog(**log)
        sr_product_log.product = sr_product

        colors: list[SRProductColor] = await get_sr_product_colors_orm_objects(
            product=sr_product,
            colors=colors_list
        )
        sizes: list[SRProductSize] = await get_sr_product_sizes_orm_objects(
            product=sr_product,
            sizes=sizes_list
        )
        to_commit.append(sr_product)
        to_commit.append(sr_product_log)
        to_commit.extend(colors)
        to_commit.extend(sizes)

    async with async_session() as session:
        session.add_all(to_commit)
        await session.commit()


async def get_sr_product_colors_orm_objects(product, colors):
    colors_orm_objects = []
    for color in colors:
        instance = SRProductColor(**color)
        instance.product = product
        colors_orm_objects.append(instance)
    return colors_orm_objects


async def get_sr_product_sizes_orm_objects(product, sizes):
    sizes_orm_objects = []
    for size in sizes:
        instance = SRProductSize(**size)
        instance.product = product
        sizes_orm_objects.append(instance)
    return sizes_orm_objects
