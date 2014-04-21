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

    export DISCOURSE_API_KEY=your_master_key
    pydiscoursecli --host=http://yourhost --api-username=system latest_topics
    pydiscoursecli --host=http://yourhost --api-username=system topics_by johnsmith
    pydiscoursecli --host=http://yourhost --api-username=system user eviltrout
