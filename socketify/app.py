import enum
import typing
import random
import string
import datetime
import logging

import msgspec
import socketify
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


ASYNC_REDIS_CLIENT: typing.Any = async_redis.Redis(host="redis")
MAIN_LOGGER: typing.Final = logging.getLogger()


async def test_simple_get(res, _) -> str:
    MAIN_LOGGER.info("Some stupid logger for improving testing complexity")
    res.end(msgspec.json.encode(VeryImportantDomainModelInput(
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
    )))


async def test_complex_api_with_db(res, _) -> dict[str, bool]:
    body = await res.get_json()
    result = await ASYNC_REDIS_CLIENT.set(f"my-key-{_create_random_string(10, 30)}", body)
    MAIN_LOGGER.info("We stored model %s  in redis with following feedback: %s", body, result)
    res.end({"ok": True})


def run_app(app: socketify.App):
    app.get("/test/simple/", test_simple_get)
    app.post("/test/complex/", test_complex_api_with_db)
