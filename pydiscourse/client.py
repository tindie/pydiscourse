"""
Core API client module
"""

import logging

import requests

from pydiscourse.exceptions import (
    DiscourseError, DiscourseServerError, DiscourseClientError)
from pydiscourse.sso import sso_payload


log = logging.getLogger('pydiscourse.client')

# HTTP verbs to be used as non string literals
DELETE = "DELETE"
GET = "GET"
POST = "POST"
PUT = "PUT"


class DiscourseClient(object):
    """Discourse API client"""

    def __init__(self, host, api_username, api_key, timeout=None):
        """
        Initialize the client

        Args:
            host: full domain name including scheme for the Discourse API
            api_username: username to connect with
            api_key: API key to connect with
            timeout: optional timeout for the request (in seconds)

        Returns:

        """
        self.host = host
        self.api_username = api_username
        self.api_key = api_key
        self.timeout = timeout

    def user(self, username):
        """
        Get user information for a specific user

        TODO: include sample data returned
        TODO: what happens when no user is found?

        Args:
            username: username to return

        Returns:
            dict of user information

        """
        return self._get('/users/{0}.json'.format(username))['user']

    def create_user(self, name, username, email, password, **kwargs):
        """
        Create a Discourse user

        Set keyword argument active='true' to avoid sending activation emails

        TODO: allow optional password and generate a random one

        Args:
            name: the full name of the new user
            username: their username (this is a key... that they can change)
            email: their email, will be used for activation and summary emails
            password: their initial password
            **kwargs: ???? what else can be sent through?

        Returns:
            ????

        """
        r = self._get('/users/hp.json')
        challenge = r['challenge'][::-1]  # reverse challenge, discourse security check
        confirmations = r['value']
        return self._post('/users', name=name, username=username, email=email,
                          password=password, password_confirmation=confirmations,
                          challenge=challenge, **kwargs)

    def user_by_external_id(self, external_id):
        """

        Args:
            external_id:

        Returns:

        """
        response = self._get("/users/by-external/{0}".format(external_id))
        return response['user']
    by_external_id = user_by_external_id

    def log_out(self, userid):
        """

        Args:
            userid:

        Returns:

        """
        return self._post('/admin/users/{0}/log_out'.format(userid))

    def trust_level(self, userid, level):
        """

        Args:
            userid:
            level:

        Returns:

        """
        return self._put('/admin/users/{0}/trust_level'.format(userid), level=level)

    def suspend(self, userid, duration, reason):
        """
        Suspend a user's account

        Args:
            userid: the Discourse user ID
            duration: the length of time in days for which a user's account
                    should be suspended
            reason: the reason for suspending the account

        Returns:
            ????

        """
        return self._put('/admin/users/{0}/suspend'.format(userid),
                         duration=duration, reason=reason)

    def unsuspend(self, userid):
        """
        Unsuspends a user's account

        Args:
            userid: the Discourse user ID

        Returns:
            None???
        """
        return self._put('/admin/users/{0}/unsuspend'.format(userid))

    def list_users(self, type, **kwargs):
        """

        optional user search: filter='test@example.com' or filter='scott'

        Args:
            type:
            **kwargs:

        Returns:

        """
        return self._get('/admin/users/list/{0}.json'.format(type), **kwargs)

    def update_avatar_from_url(self, username, url, **kwargs):
        """

        Args:
            username:
            url:
            **kwargs:

        Returns:

        """
        return self._post('/users/{0}/preferences/avatar'.format(username), file=url, **kwargs)

    def update_avatar_image(self, username, img, **kwargs):
        """

        Args:
            username:
            img:
            **kwargs:

        Returns:

        """
        files = {'file': img}
        return self._post('/users/{0}/preferences/avatar'.format(username), files=files, **kwargs)

    def toggle_gravatar(self, username, state=True, **kwargs):
        """

        Args:
            username:
            state:
            **kwargs:

        Returns:

        """
        url = '/users/{0}/preferences/avatar/toggle'.format(username)
        if bool(state):
            kwargs['use_uploaded_avatar'] = 'true'
        else:
            kwargs['use_uploaded_avatar'] = 'false'
        return self._put(url, **kwargs)

    def pick_avatar(self, username, gravatar=True, generated=False, **kwargs):
        """

        Args:
            username:
            gravatar:
            generated:
            **kwargs:

        Returns:

        """
        url = '/users/{0}/preferences/avatar/pick'.format(username)
        return self._put(url, **kwargs)

    def update_email(self, username, email, **kwargs):
        """

        Args:
            username:
            email:
            **kwargs:

        Returns:

        """
        return self._put('/users/{0}/preferences/email'.format(username), email=email, **kwargs)

    def update_user(self, username, **kwargs):
        """

        Args:
            username:
            **kwargs:

        Returns:

        """
        return self._put('/users/{0}'.format(username), **kwargs)

    def update_username(self, username, new_username, **kwargs):
        """

        Args:
            username:
            new_username:
            **kwargs:

        Returns:

        """
        return self._put('/users/{0}/preferences/username'.format(username),
                         username=new_username, **kwargs)

    def set_preference(self, username=None, **kwargs):
        """

        Args:
            username:
            **kwargs:

        Returns:

        """
        if username is None:
            username = self.api_username
        return self._put(u'/users/{0}'.format(username), **kwargs)

    def sync_sso(self, **kwargs):
        """

        expect sso_secret, name, username, email, external_id, avatar_url,
        avatar_force_update

        Args:
            **kwargs:

        Returns:

        """
        sso_secret = kwargs.pop('sso_secret')
        payload = sso_payload(sso_secret, **kwargs)
        return self._post('/admin/users/sync_sso?{0}'.format(payload), **kwargs)

    def generate_api_key(self, userid, **kwargs):
        """

        Args:
            userid:
            **kwargs:

        Returns:

        """
        return self._post('/admin/users/{0}/generate_api_key'.format(userid), **kwargs)

    def delete_user(self, userid, **kwargs):
        """

            block_email='true'
            block_ip='false'
            block_urls='false'

        Args:
            userid:
            **kwargs:

        Returns:

        """
        return self._delete('/admin/users/{0}.json'.format(userid), **kwargs)

    def users(self, filter=None, **kwargs):
        """

        Args:
            filter:
            **kwargs:

        Returns:

        """
        if filter is None:
            filter = 'active'

        return self._get('/admin/users/list/{0}.json'.format(filter), **kwargs)

    def private_messages(self, username=None, **kwargs):
        """

        Args:
            username:
            **kwargs:

        Returns:

        """
        if username is None:
            username = self.api_username
        return self._get('/topics/private-messages/{0}.json'.format(username), **kwargs)

    def private_messages_unread(self, username=None, **kwargs):
        """

        Args:
            username:
            **kwargs:

        Returns:

        """
        if username is None:
            username = self.api_username
        return self._get('/topics/private-messages-unread/{0}.json'.format(username), **kwargs)

    def hot_topics(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        return self._get('/hot.json', **kwargs)

    def latest_topics(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        return self._get('/latest.json', **kwargs)

    def new_topics(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        return self._get('/new.json', **kwargs)

    def topic(self, slug, topic_id, **kwargs):
        """

        Args:
            slug:
            topic_id:
            **kwargs:

        Returns:

        """
        return self._get('/t/{0}/{1}.json'.format(slug, topic_id), **kwargs)

    def post(self, topic_id, post_id, **kwargs):
        """

        Args:
            topic_id:
            post_id:
            **kwargs:

        Returns:

        """
        return self._get('/t/{0}/{1}.json'.format(topic_id, post_id), **kwargs)

    def posts(self, topic_id, post_ids=None, **kwargs):
        """
        Get a set of posts from a topic

        Args:
            topic_id:
            post_ids: a list of post ids from the topic stream
            **kwargs:

        Returns:

        """
        if post_ids:
            kwargs['post_ids[]'] = post_ids
        return self._get('/t/{0}/posts.json'.format(topic_id), **kwargs)

    def topic_timings(self, topic_id, time, timings={}, **kwargs):
        """
        Set time spent reading a post

        A side effect of this is to mark the post as read

        Args:
            topic_id: { post_number: ms }
            time: overall time for the topic (in what unit????)
            timings:
            **kwargs:

        Returns:

        """
        kwargs['topic_id'] = topic_id
        kwargs['topic_time'] = time
        for post_num, timing in timings.items():
            kwargs['timings[{0}]'.format(post_num)] = timing

        return self._post('/topics/timings', **kwargs)

    def topic_posts(self, topic_id, **kwargs):
        """

        Args:
            topic_id:
            **kwargs:

        Returns:

        """
        return self._get('/t/{0}/posts.json'.format(topic_id), **kwargs)

    def create_post(self, content, **kwargs):
        """

        Args:
            content:
            **kwargs:

        Returns:

        """
        return self._post('/posts', raw=content, **kwargs)

    def update_post(self, post_id, content, edit_reason='', **kwargs):
        """

        Args:
            post_id:
            content:
            edit_reason:
            **kwargs:

        Returns:

        """
        kwargs['post[raw]'] = content
        kwargs['post[edit_reason]'] = edit_reason
        return self._put('/posts/{0}'.format(post_id), **kwargs)

    def topics_by(self, username, **kwargs):
        """

        Args:
            username:
            **kwargs:

        Returns:

        """
        url = '/topics/created-by/{0}.json'.format(username)
        return self._get(url, **kwargs)['topic_list']['topics']

    def invite_user_to_topic(self, user_email, topic_id):
        """

        Args:
            user_email:
            topic_id:

        Returns:

        """
        kwargs = {
            'email': user_email,
            'topic_id': topic_id,
        }
        return self._post('/t/{0}/invite.json'.format(topic_id), **kwargs)

    def search(self, term, **kwargs):
        """

        Args:
            term:
            **kwargs:

        Returns:

        """
        kwargs['term'] = term
        return self._get('/search.json', **kwargs)

    def create_category(self, name, color, text_color='FFFFFF',
                        permissions=None, parent=None, **kwargs):
        """

        Args:
            name:
            color:
            text_color:
            permissions: dict of 'everyone', 'admins', 'moderators', 'staff' with values of ???
            parent:
            **kwargs:

        Returns:

        """
        kwargs['name'] = name
        kwargs['color'] = color
        kwargs['text_color'] = text_color

        if permissions is None and 'permissions' not in kwargs:
            permissions = {'everyone': '1'}

        for key, value in permissions.items():
            kwargs['permissions[{0}]'.format(key)] = value

        if parent:
            parent_id = None
            for category in self.categories():
                if category['name'] == parent:
                    parent_id = category['id']
                    continue

            if not parent_id:
                raise DiscourseClientError(u'{0} not found'.format(parent))
            kwargs['parent_category_id'] = parent_id

        return self._post('/categories', **kwargs)

    def categories(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        return self._get('/categories.json', **kwargs)['category_list']['categories']

    def category(self, name, parent=None, **kwargs):
        """

        Args:
            name:
            parent:
            **kwargs:

        Returns:

        """
        if parent:
            name = u'{0}/{1}'.format(parent, name)

        return self._get(u'/category/{0}.json'.format(name), **kwargs)

    def site_settings(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        for setting, value in kwargs.items():
            setting = setting.replace(' ', '_')
            self._request(PUT, '/admin/site_settings/{0}'.format(setting), {setting: value})

    def groups(self, **kwargs):
        """
        Returns a list of all groups.

        Returns:
            List of dictionaries of groups

                [
                  {
                    'alias_level': 0,
                    'automatic': True,
                    'automatic_membership_email_domains': None,
                    'automatic_membership_retroactive': False,
                    'grant_trust_level': None,
                    'has_messages': True,
                    'id': 1,
                    'incoming_email': None,
                    'mentionable': False,
                    'name': 'admins',
                    'notification_level': 2,
                    'primary_group': False,
                    'title': None,
                    'user_count': 9,
                    'visible': True
                  },
                  {
                    'alias_level': 0,
                    'automatic': True,
                    'automatic_membership_email_domains': None,
                    'automatic_membership_retroactive': False,
                    'grant_trust_level': None,
                    'has_messages': False,
                    'id': 0,
                    'incoming_email': None,
                    'mentionable': False,
                    'name': 'everyone',
                    'notification_level': None,
                    'primary_group': False,
                    'title': None,
                    'user_count': 0,
                    'visible': True
                  }
                ]

        """
        return self._get("/admin/groups.json", **kwargs)

    def add_group_owner(self, groupid, username):
        """
        Add an owner to a group by username

        Args:
            groupid: the ID of the group
            username: the new owner usernmae

        Returns:
            JSON API response

        """
        return self._put("/admin/groups/{0}/owners.json".format(groupid), usernames=username)

    def delete_group_owner(self, groupid, userid):
        """
        Deletes an owner from a group by user ID

        Does not delete the user from Discourse.

        Args:
            groupid: the ID of the group
            userid: the ID of the user

        Returns:
            JSON API response

        """
        return self._delete("/admin/groups/{0}/owners.json".format(groupid), user_id=userid)

    def add_group_member(self, groupid, username):
        """
        Add a member to a group by username

        Args:
            groupid: the ID of the group
            username: the new member usernmae

        Returns:
            JSON API response

        Raises:
            DiscourseError if user is already member of group

        """
        return self._put("/admin/groups/{0}/members.json".format(groupid), usernames=username)

    def delete_group_member(self, groupid, userid):
        """
        Deletes a member from a group by user ID

        Does not delete the user from Discourse.

        Args:
            groupid: the ID of the group
            userid: the ID of the user

        Returns:
            JSON API response

        """
        return self._delete("/admin/groups/{0}/members.json".format(groupid), user_id=userid)

    def _get(self, path, **kwargs):
        """

        Args:
            path:
            **kwargs:

        Returns:

        """
        return self._request(GET, path, kwargs)

    def _put(self, path, **kwargs):
        """

        Args:
            path:
            **kwargs:

        Returns:

        """
        return self._request(PUT, path, kwargs)

    def _post(self, path, **kwargs):
        """

        Args:
            path:
            **kwargs:

        Returns:

        """
        return self._request(POST, path, kwargs)

    def _delete(self, path, **kwargs):
        """

        Args:
            path:
            **kwargs:

        Returns:

        """
        return self._request(DELETE, path, kwargs)

    def _request(self, verb, path, params):
        """
        Executes HTTP request to API and handles response

        Args:
            verb: HTTP verb as string: GET, DELETE, PUT, POST
            path: the path on the Discourse API
            params: dictionary of parameters to include to the API

        Returns:

        """
        params['api_key'] = self.api_key
        if 'api_username' not in params:
            params['api_username'] = self.api_username
        url = self.host + path

        headers = {'Accept': 'application/json; charset=utf-8'}

        response = requests.request(
            verb, url, allow_redirects=False, params=params, headers=headers,
            timeout=self.timeout)

        log.debug('response %s: %s', response.status_code, repr(response.text))
        if not response.ok:
            try:
                msg = u','.join(response.json()['errors'])
            except (ValueError, TypeError, KeyError):
                if response.reason:
                    msg = response.reason
                else:
                    msg = u'{0}: {1}'.format(response.status_code, response.text)

            if 400 <= response.status_code < 500:
                raise DiscourseClientError(msg, response=response)

            raise DiscourseServerError(msg, response=response)

        if response.status_code == 302:
            raise DiscourseError(
                'Unexpected Redirect, invalid api key or host?', response=response)

        json_content = 'application/json; charset=utf-8'
        content_type = response.headers['content-type']
        if content_type != json_content:
            # some calls return empty html documents
            if not response.content.strip():
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
