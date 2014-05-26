#!/usr/bin/env python
import logging

import requests

from pydiscourse.exceptions import DiscourseError, DiscourseServerError, DiscourseClientError


log = logging.getLogger('pydiscourse.client')


class DiscourseClient(object):
    """ A basic client for the Discourse API that implements the raw API

    This class will attempt to remain roughly similar to the discourse_api rails API
    """
    def __init__(self, host, api_username, api_key, timeout=None):
        self.host = host
        self.api_username = api_username
        self.api_key = api_key
        self.timeout = timeout

    def user(self, username):
        return self._get('/users/{0}.json'.format(username))['user']

    def create_user(self, name, username, email, password, **kwargs):
        """ active='true', to avoid sending activation emails
        """
        r = self._get('/users/hp.json')
        challenge = r['challenge'][::-1]  # reverse challenge, discourse security check
        confirmations = r['value']
        return self._post('/users', name=name, username=username, email=email,
                  password=password, password_confirmation=confirmations, challenge=challenge, **kwargs)

    def trust_level(self, userid, level):
        return self._put('/admin/users/{0}/trust_level'.format(userid), level=level)

    def update_avatar_from_url(self, username, url, **kwargs):
        return self._post('/users/{0}/preferences/avatar'.format(username), file=url, **kwargs)

    def update_avatar_image(self, username, img, **kwargs):
        files = {'file': img}
        return self._post('/users/{0}/preferences/avatar'.format(username), files=files, **kwargs)

    def toggle_gravatar(self, username, state=True, **kwargs):
        url = '/users/{0}/preferences/avatar/toggle'.format(username)

        if bool(state):
            kwargs['use_uploaded_avatar'] = 'true'
        else:
            kwargs['use_uploaded_avatar'] = 'false'
        return self._put(url, **kwargs)

    def update_email(self, username, email, **kwargs):
        return self._put('/users/{0}/preferences/email'.format(username), email=email, **kwargs)

    def update_user(self, username, **kwargs):
        return self._put('/users/{0}'.format(username), **kwargs)

    def update_username(self, username, new_username, **kwargs):
        return self._put('/users/{0}/preferences/username'.format(username), username=new_username, **kwargs)

    def generate_api_key(self, userid, **kwargs):
        return self._post('/admin/users/{0}/generate_api_key'.format(userid), **kwargs)

    def delete_user(self, userid, **kwargs):
        """
            block_email='true'
            block_ip='false'
            block_urls='false'
        """
        return self._delete('/admin/users/{0}.json'.format(userid), **kwargs)

    def private_messages(self, username=None, **kwargs):
        if username is None:
            username = self.api_username
        return self._get('/topics/private-messages/{0}.json'.format(username), **kwargs)

    def hot_topics(self, **kwargs):
        return self._get('/hot.json', **kwargs)

    def latest_topics(self, **kwargs):
        return self._get('/latest.json', **kwargs)

    def new_topics(self, **kwargs):
        return self._get('/new.json', **kwargs)

    def topic(self, topic_id, **kwargs):
        return self._get('/t/{0}.json'.format(topic_id), **kwargs)

    def post(self, topic_id, post_id, **kwargs):
        return self._get('/t/{0}/{1}.json'.format(topic_id, post_id), **kwargs)

    def posts(self, topic_id, post_ids=None, **kwargs):
        """ Get a set of posts from a topic

        post_ids: a list of post ids from the topic stream
        """
        if post_ids:
            kwargs['post_ids[]'] = post_ids
        return self._get('/t/{0}/posts.json'.format(topic_id), **kwargs)

    def topic_timings(self, topic_id, time, timings={}, **kwargs):
        """ Set time spent reading a post

        time: overall time for the topic
        timings = { post_number: ms }

        A side effect of this is to mark the post as read
        """
        kwargs['topic_id'] = topic_id
        kwargs['topic_time'] = time
        for post_num, timing in timings.items():
            kwargs['timings[{0}]'.format(post_num)] = timing

        return self._post('/topics/timings', **kwargs)

    def topic_posts(self, topic_id, **kwargs):
        return self._get('/t/{0}/posts.json'.format(topic_id), **kwargs)

    def create_post(self, content, **kwargs):
        """ int: topic_id the topic to reply too
        """
        return self._post('/posts', raw=content, **kwargs)

    def topics_by(self, username, **kwargs):
        url = '/topics/created-by/{0}.json'.format(username)
        return self._get(url, **kwargs)['topic_list']['topics']

    def invite_user_to_topic(self, user_email, topic_id):
        kwargs = {
            'email': user_email,
            'topic_id': topic_id,
        }
        return self._post('/t/{0}/invite.json'.format(topic_id), **kwargs)

    def search(self, term, **kwargs):
        kwargs['term'] = term
        return self._get('/search.json', **kwargs)

    def categories(self, **kwargs):
        return self._get('/categories.json', **kwargs)['category_list']['categories']

    def site_settings(self, **kwargs):
        for setting, value in kwargs.items():
            setting = setting.replace(' ', '_')
            self._request('PUT', '/admin/site_settings/{0}'.format(setting), {setting: value})

    def _get(self, path, **kwargs):
        return self._request('GET', path, kwargs)

    def _put(self, path, **kwargs):
        return self._request('PUT', path, kwargs)

    def _post(self, path, **kwargs):
        return self._request('POST', path, kwargs)

    def _delete(self, path, **kwargs):
        return self._request('DELETE', path, kwargs)

    def _request(self, verb, path, params):
        params['api_key'] = self.api_key
        if 'api_username' not in params:
            params['api_username'] = self.api_username
        url = self.host + path

        response = requests.request(verb, url, allow_redirects=False, params=params, timeout=self.timeout)

        log.debug('response %s: %s', response.status_code, repr(response.text))
        if not response.ok:
            if response.reason:
                msg = response.reason
            else:
                try:
                    msg = u','.join(response.json()['errors'])
                except (ValueError, TypeError, KeyError):
                    msg = u'{0}: {1}'.format(response.status_code, response.text)

            if 400 <= response.status_code < 500:
                raise DiscourseClientError(msg, response=response)

            raise DiscourseServerError(msg, response=response)

        if response.status_code == 302:
            raise DiscourseError('Unexpected Redirect, invalid api key or host?', response=response)

        json_content = 'application/json; charset=utf-8'
        content_type = response.headers['content-type']
        if content_type != json_content:
            # some calls return empty html documents
            if response.content == ' ':
                return None

            raise DiscourseError('Invalid Response, expecting "{0}" got "{1}"'.format(
                                 json_content, content_type), response=response)

        try:
            decoded = response.json()
        except ValueError:
            raise DiscourseError('failed to decode response', response=response)

        if 'errors' in decoded:
            message = decoded.get('message')
            if not message:
                message = u','.join(decoded['errors'])
            raise DiscourseError(message, response=response)

        return decoded
