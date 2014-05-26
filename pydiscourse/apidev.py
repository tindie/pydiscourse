""" A higher level API wrapper for communicating with a Discourse instance

EXPERIMENTAL, subject to complete and radical change

Goal
------
A pythonic wrapper around the discourse API that minimizes requests by lazy loading of data.

"""
from datetime import datetime


def datetime_from(date):
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
    # XXX not handling timezone, but we're not using it yet
    return datetime.strptime(date[:-6], DATE_FORMAT)


class DiscourseUser(object):
    username = None
    userid = None
    avatar_template = None
    default_avatar_size = 40

    def avatar(self, size=None):
        if size is None:
            size = self.default_avatar_size
        return self.avatar_template.replace(u'{size}', unicode(size))

    def __repr__(self):
        return '<DiscourseUser {0} {1}>'.format(self.userid, self.username)

    @classmethod
    def from_summary(cls, summary):
        instance = cls()
        instance.username = summary['username']
        instance.userid = summary['id']
        instance.avatar_template = summary['avatar_template']

        return instance


class DiscourseUserSet(object):
    def __init__(self, users):
        self.users = users

        self.byname = {u.username: u for u in users}
        self.byid = {u.userid: u for u in users}

    def __iter__(self):
        return iter(self.users)

    def __getitem__(self, item):
        try:
            return self.byname[item]
        except KeyError:
            return self.byid[item]

    @classmethod
    def from_response(cls, response):
        users = [DiscourseUser.from_summary(u) for u in response.get('users', [])]
        return cls(users)


class DiscoursePost(object):
    default_avatar_size = 40

    def avatar(self, size=None):
        if size is None:
            size = self.default_avatar_size
        return self.avatar_template.replace(u'{size}', unicode(size))

    def date_created(self):
        return datetime_from(self.data['created_at'])

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.data = data

        return instance

    def __getattr__(self, attr):
        return self.data[attr]


class DiscourseTopic(object):
    def __init__(self):
        self.posts = None
        self.data = None
        self.raw_response = None

    def created_by(self):
        return DiscourseUser.from_summary(self.data['details']['created_by'])

    def created_at(self):
        return datetime_from(self.data['created_at'])

    def last_posted_at(self):
        return datetime_from(self.data['last_posted_at'])

    def num_unread(self):
        if self.data['unseen']:
            return 1

        return self.data['new_posts']

    def participants(self):
        return [DiscourseUser.from_summary(u) for u in self.data['participants']]

    @classmethod
    def from_response(cls, response):
        instance = DiscourseTopic.from_dict(response)
        instance.raw_response = response
        instance.posts = []
        for post in response['post_stream']['posts']:
            instance.posts.append(DiscoursePost.from_dict(post))

        return instance

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.data = data
        return instance

    def fetch_remaining_posts(self, discourse):
        """ The initial topic response is paginated, this makes another request to get additional posts
        """
        if self.data['posts_count'] > len(self.posts):
            missing = self.data['post_stream']['stream'][len(self.posts):]
            response = discourse.posts(self.id, missing)
            for post in response['post_stream']['posts']:
                self.posts.append(DiscoursePost.from_dict(post))

    def __getattr__(self, attr):
        return self.data[attr]

    def __repr__(self):
        return u'<Topic {0}>'.format(self.title)


class DiscourseTopicSet(object):
    def __init__(self, topics):
        self.topics = topics

    def all(self):
        return self.topics

    def __iter__(self):
        return iter(self.topics)

    def __len__(self):
        return len(self.topics)

    @classmethod
    def from_response(cls, response):
        topics = response.get('topic_list', {}).get('topics', [])
        topics = [DiscourseTopic.from_dict(t) for t in topics]
        return cls(topics)
