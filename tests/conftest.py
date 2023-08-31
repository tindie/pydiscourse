"""Test fixtures."""

import datetime

import pytest
from pydiscourse import client


@pytest.fixture(scope="session")
def sso_secret():
    return "d836444a9e4084d5b224a60c208dce14"


@pytest.fixture(scope="session")
def sso_nonce():
    return "cb68251eefb5211e58c00ff1395f0c0b"


@pytest.fixture(scope="session")
def sso_payload():
    return "bm9uY2U9Y2I2ODI1MWVlZmI1MjExZTU4YzAwZmYxMzk1ZjBjMGI%3D%0A"


@pytest.fixture(scope="session")
def sso_signature():
    return "2828aa29899722b35a2f191d34ef9b3ce695e0e6eeec47deb46d588d70c7cb56"


@pytest.fixture(scope="session")
def name():
    return "sam"


@pytest.fixture(scope="session")
def username():
    return "samsam"


@pytest.fixture(scope="session")
def external_id():
    return "hello123"


@pytest.fixture(scope="session")
def email():
    return "test@test.com"


@pytest.fixture(scope="session")
def redirect_url(sso_payload):
    return f"/session/sso_login?sso={sso_payload}YW0mdXNlcm5hbWU9c2Ftc2FtJmVtYWlsPXRlc3QlNDB0ZXN0LmNvbSZleHRl%0Acm5hbF9pZD1oZWxsbzEyMw%3D%3D%0A&sig=1c884222282f3feacd76802a9dd94e8bc8deba5d619b292bed75d63eb3152c0b"


@pytest.fixture(scope="session")
def discourse_host():
    return "http://testhost"


@pytest.fixture(scope="session")
def discourse_api_username():
    return "testuser"


@pytest.fixture(scope="session")
def discourse_api_key():
    return "testkey"


@pytest.fixture(scope="session")
def discourse_client(discourse_host, discourse_api_username, discourse_api_key):
    return client.DiscourseClient(
        discourse_host,
        discourse_api_username,
        discourse_api_key,
    )


@pytest.fixture
def _frozen_time(mocker):
    now = mocker.patch("pydiscourse.client.now")
    now.return_value = datetime.datetime(
        2023,
        8,
        13,
        12,
        30,
        15,
        tzinfo=datetime.timezone.utc,
    )


@pytest.fixture
def discourse_request(discourse_host, discourse_client, requests_mock):
    """Fixture for mocking Discourse API requests.

    The only request arguments are the method and the path.

    Example:

    >>> def test_something(discourse_request):
    >>>     request = discourse_request(
    >>>         "put",  # the method, case-insensitive
    >>>         "/the-path.json?q=4",  # the absolute path with query, NO host
    >>>         headers={'content-type': 'text/plain'},  # override default headers
    >>>         content=b"ERROR",  # override bytestring response
    >>>     )

    If `content` is provided, that will be used as the response body.
    If `json` is provided, then the body will return the given JSON-
        compatable Python structure (e.g. dictionary).
    If neither is given then the return `json` will be an empty
        dictionary (`{}`).

    Returns a function for inserting sensible default values.
    """

    def inner(method, path, headers=None, json=None, content=None):
        full_path = f"{discourse_host}{path}"
        if not headers:
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Api-Key": discourse_client.api_key,
                "Api-Username": discourse_client.api_username,
            }

        kwargs = {}
        if content:
            kwargs["content"] = content
        elif json:
            kwargs["json"] = json
        else:
            kwargs["json"] = {}

        return requests_mock.request(method, full_path, headers=headers, **kwargs)

    return inner
