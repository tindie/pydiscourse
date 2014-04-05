import unittest
import mock

from pydiscourse import client


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

        self.assertEqual(len(kwargs), 1)
        kwargs = kwargs['params']
        self.assertEqual(kwargs.pop('api_username'), self.api_username)
        self.assertEqual(kwargs.pop('api_key'), self.api_key)
        self.assertEqual(kwargs, params)


@mock.patch('requests.request')
class TestUser(ClientBaseTestCase):

    def test_user(self, request):
        self.client.user('someuser')
        self.assertRequestCalled(request, 'GET', '/users/someuser.json')

    def test_create_user(self, request):
        pass

    def test_activate_user(self, request):
        self.client.activate_user(22)
        self.assertRequestCalled(request, 'PUT', '/admin/users/22/activate')

    def test_activate_user_invalid_id(self, request):
        with self.assertRaises(ValueError):
            self.client.activate_user('notavaliduid')

    def test_update_email(self, request):
        email = 'test@example.com'
        self.client.update_email('someuser', email)
        self.assertRequestCalled(request, 'PUT', '/users/someuser/preferences/email', email=email)

    def test_update_user(self, request):
        self.client.update_user('someuser', a='a', b='b')
        self.assertRequestCalled(request, 'PUT', '/users/someuser', a='a', b='b')

    def test_update_username(self, request):
        self.client.update_username('someuser', 'newname')
        self.assertRequestCalled(request, 'PUT', '/users/someuser/preferences/username', username='newname')


@mock.patch('requests.request')
class TestTopics(ClientBaseTestCase):

    def test_hot_topics(self, request):
        self.client.hot_topics()
        self.assertRequestCalled(request, 'GET', '/hot.json')

    def test_latest_topics(self, request):
        self.client.latest_topics()
        self.assertRequestCalled(request, 'GET', '/latest.json')

    def test_new_topics(self, request):
        self.client.new_topics()
        self.assertRequestCalled(request, 'GET', '/new.json')

    def test_topic(self, request):
        self.client.topic(22)
        self.assertRequestCalled(request, 'GET', '/t/22.json')

    def test_topic_invalid(self, request):
        with self.assertRaises(ValueError):
            self.client.topic('notavalidtopicid')

    def test_topics_by(self, request):
        r = self.client.topics_by('someuser')
        self.assertRequestCalled(request, 'GET', '/topics/created-by/someuser.json')
        self.assertEqual(r, request().json()['topic_list']['topics'])

    def invite_user_to_topic(self, request):
        email = 'test@example.com'
        self.client.invite_user_to_topic(email, 22)
        self.assertRequestCalled(request, 'POST', '/t/22/invite.json', email=email, topic_id=22)

    def invite_user_to_topic_invalid_topic(self, request):
        with self.assertRaises(ValueError):
            self.client.invite_user_to_topic('someuser', 'invalidtopicid')


@mock.patch('requests.request')
class MiscellaneousTests(ClientBaseTestCase):

    def test_search(self, request):
        self.client.search('needle')
        self.assertRequestCalled(request, 'GET', '/search.json', term='needle')

    def test_categories(self, request):
        r = self.client.categories()
        self.assertRequestCalled(request, 'GET', '/categories.json')
        self.assertEqual(r, request().json()['category_list']['categories'])
