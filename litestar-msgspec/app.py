import sys
import enum
import typing
import random
import string
import datetime
import logging
import contextlib

import msgspec
import litestar
import redis.asyncio as async_redis


class DashboardTypes(enum.Enum):
    BIG_DASHBOARD = 1
    SMALL_DASHBOARD = 2
    COMPLEX_DASHBOARD = 3


class VeryImportantDomainModelInput(msgspec.Struct):
    user_name: typing.Annotated[str, msgspec.Meta(min_length=1, max_length=100)]
    sound_volume: typing.Annotated[int, msgspec.Meta(gt=0)]
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


@contextlib.asynccontextmanager
async def _handle_application_lifespan(application_object: litestar.Litestar):
    async_redis_client = async_redis.Redis(host="redis")
    print(f"Ping successful: {await async_redis_client.ping()}")
    application_object.state.async_redis_client = async_redis_client
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    yield
    await async_redis_client.aclose()


MAIN_LOGGER: typing.Final = logging.getLogger()


@litestar.get("/test/simple/")
async def test_simple_get() -> VeryImportantDomainModelInput:
    MAIN_LOGGER.info("Some stupid logger for improving testing complexity")
    return VeryImportantDomainModelInput(
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
    )


@litestar.post("/test/complex/")
async def test_complex_api_with_db(
    data: VeryImportantDomainModelInput,
) -> dict[str, bool]:
    result = await MAIN_APP.state.async_redis_client.set(
        f"my-key-{_create_random_string(10, 30)}", msgspec.json.encode(data)
    )
    MAIN_LOGGER.info(
        "We stored model %s  in redis with following feedback: %s",
        data,
        result,
    )
    return {"ok": True}


MAIN_APP: typing.Final = litestar.Litestar(
    route_handlers=[test_simple_get, test_complex_api_with_db, ],
    lifespan=[_handle_application_lifespan, ],
)
