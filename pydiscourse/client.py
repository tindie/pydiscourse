#!/usr/bin/env python
import requests


class DiscourseClient(object):
    def __init__(self, host, api_username, api_key):
        self.host = host
        self.api_username = api_username
        self.api_key = api_key

    def user(self, username):
        return self.get('users/{0}.json'.format(username))['user']

    def create_user(self, name, username, email, password):
        r = self.get('users/hp.json')
        challenge = r['challenge'][::-1]  # reverse challenge, discourse security check
        confirmations = r['value']
        return self.post('users', name=name, username=username, email=email,
                  password=password, password_confirmation=confirmations, challenge=challenge)

    def activate_user(self, user_id):
        return self.put('/admin/users/{0}/activate'.format(user_id))

    def hot_topics(self, **params):
        return self.get('/hot.json', **params)

    def latest_topics(self, **params):
        return self.get('/latest.json', **params)

    def new_topics(self, **params):
        return self.get('/new.json', **params)

    def topic(self, topic_id, **params):
        return self.get('/t/{0}.json'.format(topic_id), **params)

    def topics_by(self, username, **params):
        url = '/topics/created-by/{0}.json'.format(username)
        return self.get(url, **params)['topic_list']['topics']

    def invite_user_to_topic(self, user_email, topic_id):
        params = {
            'email': user_email,
            'topic_id': topic_id,
        }
        return self.post('/t/{0}/invite.json'.format(topic_id), params)

    def search(self, term, **params):
        params['term'] = term
        return self.get('/search.json', **params)

    def categories(self, **params):
        return self.get('/categories.json', **params)['category_list']['categories']

    def get(self, path, **params):
        return self._request('GET', path, params).json()

    def put(self, path, **params):
        # activate_user has no content in response, so no .json() for now
        return self._request('PUT', path, params)

    def post(self, path, **params):
        return self._request('POST', path, params).json()

    def delete(self, path, **params):
        return self._request('DELETE', path, params).json()

    def _request(self, verb, path, params):
        params['api_key'] = self.api_key
        params['api_username'] = self.api_username
        url = '{0}/{1}'.format(self.host, path)
        r = requests.request(verb, url, params=params)
        r.raise_for_status()
        return r
