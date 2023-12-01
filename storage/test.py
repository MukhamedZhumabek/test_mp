import asyncio

from dotenv import dotenv_values
from sqlalchemy import update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import BASE_DIR
from storage.models import SearchRequest

DB = dotenv_values(f'{BASE_DIR}/.env.postgres')
sqlalchemy_url = (f'postgresql+asyncpg://{DB["POSTGRES_USER"]}:{DB["POSTGRES_PASSWORD"]}@'
                  f'localhost:5433/{DB["POSTGRES_DB"]}')

engine = create_async_engine(sqlalchemy_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def bulk_update():
    ids_to_update = [1, 2, 3, 11, 10]
    update_stmt = update(SearchRequest).where(SearchRequest.local_id.in_(ids_to_update)).values(state=777)
    async with async_session() as session:
        result = await session.execute(update_stmt.returning(SearchRequest.local_id))
        await session.commit()
    updated_rows = result.scalars().fetchall()
    print("Updated Rows:", updated_rows)
    print("Error Rows:", set(ids_to_update) - set(updated_rows))

asyncio.run(bulk_update())
