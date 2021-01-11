"""
Домашнее задание №3
Асинхронная работа с сетью и бд
"""
from typing import List
import asyncio
from asyncpgsa import pg
from loguru import logger

from models import Base, User, Post, PG_CONN_URI
from jsonplaceholder_requests import fetch_users, fetch_posts


def create_tables():
    Base.metadata.create_all()


async def create_data_records(model, data: List[dict], args: dict):
    table = model.__table__
    logger.info("table {}", table)
    logger.info("process data {}", data)

    for data_row in data:
        args_values = {
            a: data_row[key]
            for a, key in args.items()
        }
        logger.info("values to set {}", args_values)
        query = table.insert().values(**args_values)
        logger.info("query {}", query)
        await pg.query(query)

    logger.info("done for {}", model)
    all_rows = await pg.query(table.select())
    logger.info("all rows for {}: {}", table, all_rows)


async def create_users(users_data: List[dict]):
    args_to_data = dict(
        id="id",
        name="name",
        username="username",
        email="email",
    )
    return await create_data_records(model=User, data=users_data, args=args_to_data)


async def create_posts(posts_data: List[dict]):
    args_to_data = dict(
        id="id",
        user_id="userId",
        title="title",
        body="body",
    )
    return await create_data_records(model=Post, data=posts_data, args=args_to_data)


async def clear_tables():
    await pg.query(Post.__table__.delete())
    await pg.query(User.__table__.delete())


async def create_all_records():
    await pg.init(PG_CONN_URI)
    await clear_tables()

    # task_users_data = asyncio.create_task(fetch_users(), name="users_data")
    # task_posts_data = asyncio.create_task(fetch_posts(), name="posts_data")
    #
    # done, pending = await asyncio.wait(
    #     {task_users_data, task_posts_data},
    #     timeout=10,
    #     return_when=asyncio.ALL_COMPLETED,
    # )

    users_data = await fetch_users()
    await create_users(users_data)
    posts_data = await fetch_posts()
    await create_posts(posts_data)

    await pg.pool.close()


def main():
    create_tables()
    asyncio.run(create_all_records())


if __name__ == "__main__":
    main()
