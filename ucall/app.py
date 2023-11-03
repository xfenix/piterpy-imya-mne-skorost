import typing
import enum
import typing
import random
import string
import logging
import datetime

import pydantic
# from ucall.uring import Server as UcallServer
from ucall.posix import Server as UcallServer


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


MAIN_LOGGER: typing.Final = logging.getLogger()
MAIN_SERVER_APP: typing.Final = UcallServer()


@MAIN_SERVER_APP
def sum():
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


if __name__ == "__main__":
    MAIN_SERVER_APP.run()
