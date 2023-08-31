"""Tests for the client methods."""

import urllib.parse

import pytest


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
    def test_get_user(self, discourse_host, discourse_client, discourse_request):
        request = discourse_request(
            "get",
            "/users/someuser.json",
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
            "Test User",
            "testuser",
            "test@example.com",
            "notapassword",
        )

        assert session_request.called_once
        assert user_request.called_once

    def test_update_email(self, discourse_host, discourse_client, discourse_request):
        request = discourse_request("put", "/users/someuser/preferences/email")
        discourse_client.update_email("someuser", "newmeail@example.com")

        assert request.called_once

    def test_update_user(self, discourse_client, discourse_request):
        request = discourse_request("put", "/users/someuser")
        discourse_client.update_user("someuser", a="a", b="b")

        assert request.called_once

    def test_update_username(self, discourse_client, discourse_request):
        request = discourse_request("put", "/users/someuser/preferences/username")
        discourse_client.update_username("someuser", "newname")

        assert request.called_once

    def test_by_external_id(self, discourse_client, discourse_request):
        request = discourse_request(
            "get",
            "/users/by-external/123",
            json={"user": "123"},
        )
        discourse_client.by_external_id(123)

        assert request.called_once

    @pytest.mark.usefixtures("_frozen_time")
    def test_suspend_user(self, discourse_client, discourse_request):
        request = discourse_request("put", "/admin/users/123/suspend")
        discourse_client.suspend(123, 1, "Testing")

        assert request.called_once
        assert request.last_request.method == "PUT"

        request_payload = urllib.parse.parse_qs(request.last_request.text)

        assert request_payload["reason"] == ["Testing"]
        assert request_payload["suspend_until"] == ["2023-08-14T12:30:15+00:00"]

    def test_unsuspend_user(self, discourse_client, discourse_request):
        request = discourse_request("put", "/admin/users/123/unsuspend")
        discourse_client.unsuspend(123)

        assert request.called_once

    def test_user_bagdes(self, discourse_client, discourse_request):
        request = discourse_request("get", "/user-badges/myusername.json")
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


class TestEverything:
    def test_latest_posts(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/posts.json?before=54321",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.latest_posts(before=54321)
        assert request.called_once

    def test_search(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/search.json?term=needle",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.search(term="needle")
        assert request.called_once

    def test_categories(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/categories.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"category_list": {"categories": []}},
        )
        discourse_client.categories()
        assert request.called_once

    def test_update_category(self, discourse_client, requests_mock):
        # self.assertRequestCalled(request, "PUT", "/categories/123", a="a", b="b")
        request = requests_mock.put(
            f"{discourse_client.host}/categories/123",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.update_category(123, a="a", b="b")

        request_payload = request.last_request.json()

        assert request_payload["a"] == "a"
        assert request_payload["b"] == "b"

    def test_users(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/admin/users/list/active.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.users()
        assert request.called_once

    def test_badges(self, discourse_client, requests_mock):
        request = requests_mock.get(
            f"{discourse_client.host}/admin/badges.json",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.badges()
        assert request.called_once

    def test_grant_badge_to(self, discourse_client, requests_mock):
        request = requests_mock.post(
            f"{discourse_client.host}/user_badges",
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={},
        )
        discourse_client.grant_badge_to("username", 1)

        request_payload = urllib.parse.parse_qs(request.last_request.text)

        assert request_payload["username"] == ["username"]
        assert request_payload["badge_id"] == ["1"]
