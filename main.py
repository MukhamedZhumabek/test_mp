from logging import getLogger


from fastapi import FastAPI
from pydantic import BaseModel

from app.search_by_query.fetcher import get_by_query
from app.search_by_query.producer import produce
from app.search_by_query.consumer import consume

from settings import setup_logging

setup_logging()

logger = getLogger('app.main')
app = FastAPI()


class ApiResponse(BaseModel):
    status: int
    result: str
    msg: str


@app.get('/fetcher', response_model=ApiResponse)
async def producer():
    try:
        await get_by_query()
        result = {'status': 0, 'result': 'ok', 'msg': ''}
    except Exception as e:
        result = {'status': 1, 'result': '', 'msg': str(e)}
    return ApiResponse(**result)


@app.get('/producer', response_model=ApiResponse)
async def producer():
    try:
        await produce()
        result = {'status': 0, 'result': 'ok', 'msg': ''}
    except Exception as e:
        result = {'status': 1, 'result': '', 'msg': str(e)}
    return ApiResponse(**result)


@app.get('/consumer', response_model=ApiResponse)
async def consumer():
    try:
        await consume()
        result = {'status': 0, 'result': 'ok', 'msg': ''}
    except Exception as e:
        result = {'status': 1, 'result': '', 'msg': str(e)}
    return ApiResponse(**result)
