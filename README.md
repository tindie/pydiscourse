pydiscourse
------------
A Python library for the Discourse API.
Its pretty basic right now but you need to start somewhere.


Examples
-----------
Create a client connection to a Discourse server::

    from pydiscourse.client import DiscourseClient
    client = DiscourseClient('http://example.com', api_username='username', api_key='areallylongstringfromdiscourse')

Get info about a user::

    user = client.user('eviltrout')
    print user

    user_topics = client.topics_by('johnsmith')
    print user_topics

Create a new user::

    user = client.create_user('The Black Knight', 'blacknight', 'knight@python.org', 'justafleshwound')

Command line
----------------

To help experiment with the Discourse API, pydiscourse provides a simple command line client::

    pydiscourse --host=http://yourhost --api-username=system --api-key=API_KEY latest_topics
    pydiscourse --host=http://yourhost --api-username=system --api-key=API_KEY topics_by johnsmith
    pydiscourse --host=http://yourhost --api-username=system --api-key=API_KEY user eviltrout
