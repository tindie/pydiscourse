pydiscourse
===========

A Python library for the Discourse API


# Command line
To help inspect and experiment with the Discourse API pydiscourse provides a simple command line client.

    pydiscourse --host=http://yourhost --api-username=system --api-key=API_KEY latest_topics
    pydiscourse --host=http://yourhost --api-username=system --api-key=API_KEY topics_by johnsmith
    pydiscourse --host=http://yourhost --api-username=system --api-key=API_KEY user eviltrout

# Development

## Live Testing
You can test against a Discourse instance by following the [Official Discourse developement instructions][discoursedev].
For the impatient here is the quick and dirty version:

    git clone git@github.com:discourse/discourse.git
    cd discourse
    vagrant up
    vagrant ssh
    cd /vagrant
    bundle install
    bundle exec rake db:migrate
    bundle exec rails s

Once running you can access the Discourse install at http://localhost:4000.

[discoursedev]: https://github.com/discourse/discourse/blob/master/docs/VAGRANT.md "Discourse Vagrant"
