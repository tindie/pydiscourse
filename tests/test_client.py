import unittest
import mock

from pydiscourse import client


def prepare_response(request):
    # we need to mocked response to look a little more real
    request.return_value = mock.MagicMock(headers={'content-type': 'application/json; charset=utf-8'})


class ClientBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.host = 'testhost'
        self.api_username = 'testuser'
        self.api_key = 'testkey'

        self.client = client.DiscourseClient(self.host, self.api_username, self.api_key)

    def assertRequestCalled(self, request, verb, url, **params):
        self.assertTrue(request.called)

        args, kwargs = request.call_args

        self.assertEqual(args[0], verb)
        self.assertEqual(args[1], self.host + url)

        kwargs = kwargs['params']
        self.assertEqual(kwargs.pop('api_username'), self.api_username)
        self.assertEqual(kwargs.pop('api_key'), self.api_key)
        self.assertEqual(kwargs, params)


@mock.patch('requests.request')
class TestUser(ClientBaseTestCase):

    def test_user(self, request):
        prepare_response(request)
        self.client.user('someuser')
        self.assertRequestCalled(request, 'GET', '/users/someuser.json')

    def test_create_user(self, request):
        prepare_response(request)
        self.client.create_user('Test User', 'testuser', 'test@example.com', 'notapassword')
        self.assertEqual(request.call_count, 2)
        # XXX incomplete

    def test_update_email(self, request):
        prepare_response(request)
        email = 'test@example.com'
        self.client.update_email('someuser', email)
        self.assertRequestCalled(request, 'PUT', '/users/someuser/preferences/email', email=email)

    def test_update_user(self, request):
        prepare_response(request)
        self.client.update_user('someuser', a='a', b='b')
        self.assertRequestCalled(request, 'PUT', '/users/someuser', a='a', b='b')

    def test_update_username(self, request):
        prepare_response(request)
        self.client.update_username('someuser', 'newname')
        self.assertRequestCalled(request, 'PUT', '/users/someuser/preferences/username', username='newname')


@mock.patch('requests.request')
class TestTopics(ClientBaseTestCase):

    def test_hot_topics(self, request):
        prepare_response(request)
        self.client.hot_topics()
        self.assertRequestCalled(request, 'GET', '/hot.json')

    def test_latest_topics(self, request):
        prepare_response(request)
        self.client.latest_topics()
        self.assertRequestCalled(request, 'GET', '/latest.json')

    def test_new_topics(self, request):
        prepare_response(request)
        self.client.new_topics()
        self.assertRequestCalled(request, 'GET', '/new.json')

    def test_topic(self, request):
        prepare_response(request)
        self.client.topic(22)
        self.assertRequestCalled(request, 'GET', '/t/22.json')

    def test_topics_by(self, request):
        prepare_response(request)
        r = self.client.topics_by('someuser')
        self.assertRequestCalled(request, 'GET', '/topics/created-by/someuser.json')
        self.assertEqual(r, request().json()['topic_list']['topics'])

    def invite_user_to_topic(self, request):
        prepare_response(request)
        email = 'test@example.com'
        self.client.invite_user_to_topic(email, 22)
        self.assertRequestCalled(request, 'POST', '/t/22/invite.json', email=email, topic_id=22)


@mock.patch('requests.request')
class MiscellaneousTests(ClientBaseTestCase):

    def test_search(self, request):
        prepare_response(request)
        self.client.search('needle')
        self.assertRequestCalled(request, 'GET', '/search.json', term='needle')

    def test_categories(self, request):
        prepare_response(request)
        r = self.client.categories()
        self.assertRequestCalled(request, 'GET', '/categories.json')
        self.assertEqual(r, request().json()['category_list']['categories'])
