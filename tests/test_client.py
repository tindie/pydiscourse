import unittest
import urllib.parse
from unittest import mock

from pydiscourse import client


def test_empty_content_http_ok(discourse_host, discourse_client, requests_mock):
    """Empty content should not raise error

    Critical to test against *bytestrings* rather than unicode
    """
    requests_mock.get(
        f"{discourse_host}/users/admin/1/unsuspend",
        headers={"Content-Type": "text/plain; charset=utf-8"},
        content=b" ",
    )

    resp = discourse_client._request("GET", "/users/admin/1/unsuspend", {})

    assert resp is None


class TestUserManagement:
    def test_get_user(self, discourse_host, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_host}/users/someuser.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"user": "someuser"},
        )
        discourse_client.user("someuser")
        assert request.called_once

    def test_create_user(self, discourse_host, discourse_client, requests_mock):
        session_request = requests_mock.get(
            f"{discourse_host}/session/hp.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"challenge": "challenge", "value": "value"},
        )
        user_request = requests_mock.post(
            f"{discourse_host}/users",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.create_user(
            "Test User", "testuser", "test@example.com", "notapassword"
        )

        assert session_request.called_once
        assert user_request.called_once

    def test_update_email(self, discourse_host, discourse_client, requests_mock):
        request = requests_mock.put(
            f"{discourse_host}/users/someuser/preferences/email",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.update_email("someuser", "newmeail@example.com")

        assert request.called_once

    def test_update_user(self, discourse_client, requests_mock):
        request = requests_mock.put(
            f"{discourse_client.host}/users/someuser",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.update_user("someuser", a="a", b="b")

        assert request.called_once

    def test_update_username(self, discourse_client, requests_mock):
        request = requests_mock.put(
            f"{discourse_client.host}/users/someuser/preferences/username",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.update_username("someuser", "newname")

        assert request.called_once

    def test_by_external_id(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/users/by-external/123",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"user": "123"},
        )
        discourse_client.by_external_id(123)

        assert request.called_once

    def test_suspend_user(self, discourse_client, requests_mock, frozen_time):
        request = requests_mock.put(
            f"{discourse_client.host}/admin/users/123/suspend",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.suspend(123, 1, "Testing")

        assert request.called_once
        assert request.last_request.method == "PUT"

        request_payload = urllib.parse.parse_qs(request.last_request.text)

        assert request_payload["reason"] == ["Testing"]
        assert request_payload["suspend_until"] == ["2023-08-14T12:30:15+00:00"]

    def test_unsuspend_user(self, discourse_client, requests_mock):
        request = requests_mock.put(
            f"{discourse_client.host}/admin/users/123/unsuspend",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.unsuspend(123)

        assert request.called_once

    def test_user_bagdes(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/user-badges/myusername.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.user_badges("myusername")

        assert request.called_once


class TestTopics:
    def test_hot_topics(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/hot.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.hot_topics()
        assert request.called_once

    def test_latest_topics(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/latest.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.latest_topics()

        assert request.called_once

    def test_new_topics(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/new.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.new_topics()
        assert request.called_once

    def test_topic(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/t/some-test-slug/22.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.topic("some-test-slug", 22)
        assert request.called_once

    def test_topics_by(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/topics/created-by/someuser.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"topic_list": {"topics": []}},
        )
        discourse_client.topics_by("someuser")

        assert request.called_once

    def test_invite_user_to_topic(self, discourse_client, requests_mock):
        request = requests_mock.post(
            f"{discourse_client.host}/t/22/invite.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.invite_user_to_topic("test@example.com", 22)
        assert request.called_once

        request_payload = urllib.parse.parse_qs(request.last_request.text)

        assert request_payload["email"] == ["test@example.com"]
        assert request_payload["topic_id"] == ["22"]


def prepare_response(request):
    # we need to mocked response to look a little more real
    request.return_value = mock.MagicMock(
        headers={"content-type": "application/json; charset=utf-8"}
    )


class ClientBaseTestCase(unittest.TestCase):
    """ """

    def setUp(self):
        self.host = "http://testhost"
        self.api_username = "testuser"
        self.api_key = "testkey"

        self.client = client.DiscourseClient(self.host, self.api_username, self.api_key)

    def assertRequestCalled(self, request, verb, url, **params):
        self.assertTrue(request.called)

        args, kwargs = request.call_args

        self.assertEqual(args[0], verb)
        self.assertEqual(args[1], self.host + url)

        headers = kwargs["headers"]
        self.assertEqual(headers.pop("Api-Username"), self.api_username)
        self.assertEqual(headers.pop("Api-Key"), self.api_key)

        if verb == "GET":
            self.assertEqual(kwargs["params"], params)


@mock.patch("pydiscourse.client.requests.request")
class MiscellaneousTests(ClientBaseTestCase):
    def test_latest_posts(self, request):
        prepare_response(request)
        r = self.client.latest_posts(before=54321)
        self.assertRequestCalled(request, "GET", "/posts.json", before=54321)

    def test_search(self, request):
        prepare_response(request)
        self.client.search("needle")
        self.assertRequestCalled(request, "GET", "/search.json", term="needle")

    def test_categories(self, request):
        prepare_response(request)
        r = self.client.categories()
        self.assertRequestCalled(request, "GET", "/categories.json")
        self.assertEqual(r, request().json()["category_list"]["categories"])

    def test_update_category(self, request):
        prepare_response(request)
        self.client.update_category(123, a="a", b="b")
        self.assertRequestCalled(request, "PUT", "/categories/123", a="a", b="b")

    def test_users(self, request):
        prepare_response(request)
        self.client.users()
        self.assertRequestCalled(request, "GET", "/admin/users/list/active.json")

    def test_badges(self, request):
        prepare_response(request)
        self.client.badges()
        self.assertRequestCalled(request, "GET", "/admin/badges.json")

    def test_grant_badge_to(self, request):
        prepare_response(request)
        self.client.grant_badge_to("username", 1)
        self.assertRequestCalled(
            request, "POST", "/user_badges", username="username", badge_id=1
        )
