import sys
import enum
import typing
import random
import string
import datetime
import logging

import robyn
import msgspec
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


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
ASYNC_REDIS_CLIENT: typing.Final = async_redis.Redis(host="redis")
MAIN_APP: typing.Final = robyn.Robyn(__file__)
MAIN_LOGGER: typing.Final = logging.getLogger()


@MAIN_APP.get("/test/simple/")
async def test_simple_get(_) -> VeryImportantDomainModelInput:
    MAIN_LOGGER.info("Some stupid logger for improving testing complexity")
    return robyn.Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        description=msgspec.json.encode(
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
            )
        ),
    )


@MAIN_APP.post("/test/complex/")
async def test_complex_api_with_db(request: robyn.Request) -> dict[str, bool]:
    something_important_to_us: VeryImportantDomainModelInput = (
        VeryImportantDomainModelInput(**request.json())
    )
    result = await ASYNC_REDIS_CLIENT.set(
        f"my-key-{_create_random_string(10, 30)}",
        msgspec.json.encode(something_important_to_us),
    )
    MAIN_LOGGER.info(
        "We stored model %s  in redis with following feedback: %s",
        something_important_to_us,
        result,
    )
    return robyn.jsonify({"ok": True})


if __name__ == "__main__":
    MAIN_APP.start(host="0.0.0.0", port="80")
