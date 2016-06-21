pydiscourse
------------
A Python library for working with Discourse.

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

Implement SSO for Discourse with your Python server::

    @login_required
    def discourse_sso_view(request):
        payload = request.GET.get('sso')
        signature = request.GET.get('sig')
        nonce = sso_validate(payload, signature, SECRET)
        url = sso_redirect_url(nonce, SECRET, request.user.email, request.user.id, request.user.username)
        return redirect('http://discuss.example.com' + url)

Command line
----------------

To help experiment with the Discourse API, pydiscourse provides a simple command line client::

    export DISCOURSE_API_KEY=your_master_key
    pydiscoursecli --host=http://yourhost --api-user=system latest_topics
    pydiscoursecli --host=http://yourhost --api-user=system topics_by johnsmith
    pydiscoursecli --host=http://yourhost --api-user=system user eviltrout
