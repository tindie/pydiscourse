#!/usr/bin/env python
import logging

import requests


log = logging.getLogger('pydiscourse.client')

HTTPError = requests.HTTPError


class DiscourseAPIError(Exception):
    pass


class DiscourseClient(object):
    """ A basic client for the Discourse API that implements the raw API
    """
    def __init__(self, host, api_username, api_key):
        self.host = host
        self.api_username = api_username
        self.api_key = api_key

    def user(self, username):
        return self.get('/users/{0}.json'.format(username))['user']

    def create_user(self, name, username, email, password='', **kwargs):
        """ active='true', to avoid sending activation emails
        """
        r = self.get('/users/hp.json')
        challenge = r['challenge'][::-1]  # reverse challenge, discourse security check
        confirmations = r['value']
        return self.post('/users', name=name, username=username, email=email,
                  password=password, password_confirmation=confirmations, challenge=challenge, **kwargs )

    def activate_user(self, user_id):
        return self.put('/admin/users/{0}/activate'.format(user_id))

    def update_avatar(self, username, avatar):
        """
        avatar: URL pointing to the image for the users avatar

        XXX should be able to pass in the bytes for an image but it doesn't seem to be working properly
        """
        return self.post('/users/{0}/preferences/avatar'.format(username), file=avatar)

    def update_email(self, username, email):
        return self.put('/users/{0}/preferences/email'.format(username), email=email)

    def update_user(self, username, **kwargs):
        return self.put('/users/{0}'.format(username), **kwargs)

    def update_username(self, username, new_username):
        return self.put('/users/{0}/preferences/username'.format(username), username=new_username)

    def hot_topics(self, **kwargs):
        return self.get('/hot.json', **kwargs)

    def latest_topics(self, **kwargs):
        return self.get('/latest.json', **kwargs)

    def new_topics(self, **kwargs):
        return self.get('/new.json', **kwargs)

    def topic(self, topic_id, **kwargs):
        return self.get('/t/{0}.json'.format(topic_id), **kwargs)

    def create_post(self, content, **kwargs):
        return self.post('/posts', raw=content, archtype='regular', **kwargs)

    def topics_by(self, username, **kwargs):
        url = '/topics/created-by/{0}.json'.format(username)
        return self.get(url, **kwargs)['topic_list']['topics']

    def invite_user_to_topic(self, user_email, topic_id):
        kwargs = {
            'email': user_email,
            'topic_id': topic_id,
        }
        return self.post('/t/{0}/invite.json'.format(topic_id), **kwargs)

    def search(self, term, **kwargs):
        kwargs['term'] = term
        return self.get('/search.json', **kwargs)

    def categories(self, **kwargs):
        return self.get('/categories.json', **kwargs)['category_list']['categories']

    def site_settings(self, **kwargs):
        for setting, value in kwargs.items():
            setting = setting.replace(' ', '_')
            self._request('PUT', '/admin/site_settings/{0}'.format(setting), {setting: value})

    def get(self, path, **kwargs):
        return self._request('GET', path, kwargs)

    def put(self, path, **kwargs):
        return self._request('PUT', path, kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, kwargs)

    def _request(self, verb, path, params):
        params['api_key'] = self.api_key
        params['api_username'] = self.api_username
        url = self.host + path
        response = requests.request(verb, url, params=params)
        log.debug('response %s: %s', response.status_code, repr(response.text))
        try:
            response.raise_for_status()
        except HTTPError:
            if not response.reason:
                try:
                    response.reason = response.json()['errors']
                except (ValueError, KeyError):
                    response.reason = response.text
                response.raise_for_status()
            raise

        # activate_user has no content in response, so no/u .json() for now
        if not response.content or response.content == ' ':
            return None

        decoded = response.json()
        if 'errors' in decoded:
            raise DiscourseAPIError(decoded['errors'])

        return decoded
