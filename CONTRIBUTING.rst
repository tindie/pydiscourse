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

Pull requests
=============

Reviewing and merging pull requests is work, so whatever you can do to make this
easier for the package maintainer not only speed up the process of getting your
changes merged but also ensure they are. These few guidelines help significantly.
If they are confusing or you need help understanding how to accomplish them,
please ask for help in an issue. 

- Please do make sure your chnageset represents a *discrete update*. If you would like to fix formatting, by all means, but don't mix that up with a bug fix. Those are separate PRs.
- Please do make sure that both your pull request description and your commits are meaningful and descriptive. Rebase first, if need be.
- Please do make sure your changeset does not include more commits than necessary. Rebase first, if need be.
- Please do make sure the changeset is not very big. If you have a large change propose it in an issue first.
- Please do make sure your changeset is based on a branch from the current HEAD of the fork you wish to merge against. This is a general best practice. Rebase first, if need be.

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

For a list of all operations:

    you can just run rake routes inside of the discourse repo to get an up to date list

Or check the old [`routes.txt`](https://github.com/discourse/discourse_api/blob/aa75df6cd851f0666f9e8071c4ef9dfdd39fc8f8/routes.txt) file, though this is certainly outdated.
