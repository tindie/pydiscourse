"""Test fixtures."""

import pytest


@pytest.fixture
def secret():
    return "d836444a9e4084d5b224a60c208dce14"


@pytest.fixture
def nonce():
    return "cb68251eefb5211e58c00ff1395f0c0b"


@pytest.fixture
def payload():
    return "bm9uY2U9Y2I2ODI1MWVlZmI1MjExZTU4YzAwZmYxMzk1ZjBjMGI%3D%0A"


@pytest.fixture
def signature():
    return "2828aa29899722b35a2f191d34ef9b3ce695e0e6eeec47deb46d588d70c7cb56"


@pytest.fixture
def name():
    return "sam"


@pytest.fixture
def username():
    return "samsam"


@pytest.fixture
def external_id():
    return "hello123"


@pytest.fixture
def email():
    return "test@test.com"


@pytest.fixture
def redirect_url():
    return "/session/sso_login?sso=bm9uY2U9Y2I2ODI1MWVlZmI1MjExZTU4YzAwZmYxMzk1ZjBjMGImbmFtZT1z%0AYW0mdXNlcm5hbWU9c2Ftc2FtJmVtYWlsPXRlc3QlNDB0ZXN0LmNvbSZleHRl%0Acm5hbF9pZD1oZWxsbzEyMw%3D%3D%0A&sig=1c884222282f3feacd76802a9dd94e8bc8deba5d619b292bed75d63eb3152c0b"
