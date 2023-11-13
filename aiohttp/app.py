import sys
import enum
import json
import typing
import random
import string
import datetime
import logging
import functools

import pydantic
import redis.asyncio as async_redis
from aiohttp import web


class DashboardTypes(enum.Enum):
    BIG_DASHBOARD = 1
    SMALL_DASHBOARD = 2
    COMPLEX_DASHBOARD = 3


class VeryImportantDomainModelInput(pydantic.BaseModel):
    user_name: typing.Annotated[str, pydantic.Field(min_length=1, max_length=100)]
    sound_volume: typing.Annotated[int, pydantic.Field(gt=0, example=10)]
    score: int
    type_of_dashboard: DashboardTypes
    when: datetime.datetime


def _create_random_string(min_length, max_length) -> str:
    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=random.randint(min_length, max_length),
        )
    )


async def _handle_application_lifespan(application_object: web.Application):
    async_redis_client = async_redis.Redis(host="redis")
    print(f"Ping successful: {await async_redis_client.ping()}")
    application_object["async_redis_client"] = async_redis_client
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    yield
    await async_redis_client.aclose()


MAIN_LOGGER: typing.Final = logging.getLogger()


async def test_simple_get(_: web.Request) -> web.Response:
    MAIN_LOGGER.info("Some stupid logger for improving testing complexity")
    return web.json_response(
        VeryImportantDomainModelInput(
            user_name=f"Privet. Kak dela? My name is: {_create_random_string(20, 70)}",
            sound_volume=random.randint(1, 100),
            score=random.randint(1_000, 1_000_000),
            type_of_dashboard=random.choice(
                (
                    DashboardTypes.BIG_DASHBOARD,
                    DashboardTypes.SMALL_DASHBOARD,
                    DashboardTypes.COMPLEX_DASHBOARD,
                )
            ),
            when=datetime.datetime.now(),
        ).model_dump(),
        dumps=functools.partial(json.dumps, default=str)  # this is wrong, but im tired
    )


async def test_complex_api_with_db(request: web.Request) -> web.Response:
    something_important_to_us: typing.Final = VeryImportantDomainModelInput(**await request.json())
    result = await request.app["async_redis_client"].set(
        f"my-key-{_create_random_string(10, 30)}", something_important_to_us.json()
    )
    MAIN_LOGGER.info(
        "We stored model %s  in redis with following feedback: %s",
        something_important_to_us,
        result,
    )
    return web.json_response({"ok": True})


MAIN_APP: typing.Final = web.Application()
MAIN_APP.cleanup_ctx.append(_handle_application_lifespan)
MAIN_APP.add_routes([
    web.get("/test/simple/", test_simple_get),
    web.post("/test/complex/", test_complex_api_with_db)
])
