.. :changelog:

Release history
===============

1.2.0
-----

- BREAKING? Dropped support for Python 2.7, 3.4, 3.5
- Added numerous new endpoint queries
- Updated category querying

1.1.2
-----

- Fix for Discourse users API change

1.1.1
-----

- Fix for empty dictionary and 413 API response
- Fix for getting member groups

1.1.0
-----

- Added ability to follow redirects in requests

1.0.0
-----

- Authenticate with headers

0.9.0
-----

- Added rate limiting support
- Added some support for user activation

0.8.0
-----

- Add some PR guidance
- Add support for files in the core request methods
- Adds numerous new API controls, including:
   - tag_group
   - user_actions
   - upload_image
   - block
   - trust_level_lock
   - create_site_customization (theme)
   - create_color_scheme
   - color_schemes
   - add_group_members
   - group_members
   - group_owners
   - delete_group
   - create_group
   - group
   - customize_site_texts
   - delete_category
   - user_emails
   - update_topic_status
   - create_post
   - update_topic
   - update_avatar
   - user_all


0.7.0
-----

* Place request parameters in the request body for POST and PUT requests.
  Allows larger request sizes and solves for `URI Too Large` error.

0.6.0
-----

* Adds method to add user to group by user ID

0.5.0
-----

* Adds badges functionality

0.4.0
-----

* Adds initial groups functionality

0.3.2
-----

* SSO functionality fixes

0.3.1
-----

* Fix how empty responses are handled

0.3.0
-----

* Added method to unsuspend suspended user

0.2.0
-----

* Inital fork, including gberaudo's changes
* Packaging cleanup, dropping Python 2.6 support and adding Python 3.5, PyPy,
  PyPy3
* Packaging on PyPI

0.1.0.dev
---------

All pre-PyPI development

