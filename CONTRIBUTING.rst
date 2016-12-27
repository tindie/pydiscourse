============
Contributing
============

For patches, please ensure that all existing tests pass, that you have adequate
tests added as necessary, and that all code is documented! The latter is
critical. If you add or update an existing function, class, or module, please
ensure you add a docstring or ensure the existing docstring is up-to-date.

Please use `Google docstring format
<http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html>`_.

This *will* be enforced.

Testing
=======

The best way to run the tests is with `tox <http://tox.readthedocs.org/en/latest/>`_::

    pip install tox
    detox

Or it's slightly faster cousin `detox
<https://pypi.python.org/pypi/detox>`_ which will parallelize test runs::

    pip install detox
    detox

Alternatively, you can run the self test with the following commands::

    pip install -r requirements.dev.txt
    pip install -e .
    python setup.py test

Live Testing
============

You can test against a Discourse instance by following the [Official Discourse developement instructions][discoursedev].
For the impatient here is the quick and dirty version::

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

TODO
====

Refer to, https://github.com/discourse/discourse_api/blob/master/routes.txt for
a list of all operations available in Discourse.
