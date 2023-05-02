=============
superset-okta
=============


.. image:: https://img.shields.io/pypi/v/superset_okta.svg
        :target: https://pypi.python.org/pypi/superset_okta

.. image:: https://img.shields.io/travis/amartincolville/superset_okta.svg
        :target: https://travis-ci.com/amartincolville/superset_okta

.. image:: https://readthedocs.org/projects/superset-okta/badge/?version=latest
        :target: https://superset-okta.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


A Python package to integrate Okta integration as a provider for authenticating in Superset.

The custom provider methods can be modified according to your own company/usage rules.


Prerequisites
--------

Set up a Superset application within Okta. To do so:

1. In the Admin Console, go to Applications.
2. Click Create App Integration.
3. To create an OIDC app integration, select OIDC - OpenID Connect as the Sign-in method.
4. Select Web Application.
5. Click Next.
6. In general settings:
    a. specify the name of the application, choose a logo and select `Client acting on behalf of user` as Grant type;
    b. tick the `Authorization Code`, `Refresh Token`, `Implicit (hybrid)` boxes, and both `Allow ID Token with implicit grant type` and `Allow Access Token with implicit grant type`.
7. Use persistent token as Refresh Token.
8. Add your Sign-in redirect URIs. It should look something like `https://<your_superset_domain>.com/oauth-authorized/okta`
9. Sign-out redirect URIs: `https://<your_superset_domain>.com`
10. Login initiated by `Either Okta or App.`
11. Initiate login URI `https://<your_superset_domain>.com/login`
12. Token credentials should be set to `Automatic`.
13. OpenID Connect ID Token can include a regex if you are using prefixes in your groups. To obtain all groups, add ``.*`` as the regex in the `Groups claim filter` with the Matches regex condition.
14. In the Assignments tab, you can include all your groups that should be entitled to use Superset. You should at least include the `Superset_Admin` and `Superset_Explorer` groups - if you follow the same logic as the one provided.

Usage
--------

1. Go to your Superset config file: `config.py`.
2. Import the security manager::

    from superset_okta import provider

3. Set up the ``OKTA_BASE_URL``, ``OKTA_CLIENT_ID`` and ``OKTA_SECRET`` environment variables. The details on these should be in your `Okta application <https://developer.okta.com/docs/guides/find-your-app-credentials/main/>`__.

4. Include the following code snippet in your config file::

    # OKTA_BASE_URL must be
    #    https://{yourOktaDomain}/oauth2/v1/ (okta authorization server)
    # Cannot be
    #    https://{yourOktaDomain}/oauth2/default/v1/ (custom authorization server)
    # Otherwise you won't be able to obtain Groups info.
    OKTA_BASE_URL = os.getenv("OKTA_BASE_URL")
    OAUTH_PROVIDERS = [
        {
            "name": "okta",
            "token_key": "access_token",
            "icon": "fa-circle-o",
            "remote_app": {
                "client_id": os.getenv("OKTA_CLIENT_ID"),
                "client_secret": os.getenv("OKTA_SECRET"),
                "api_base_url": OKTA_BASE_URL,
                "client_kwargs": {"scope": "openid profile email groups"},
                "request_token_url": None,
                "access_token_url": OKTA_BASE_URL + "token",
                "authorize_url": OKTA_BASE_URL + "authorize",
                "jwks_uri": OKTA_BASE_URL + "keys",
            },
        }
    ]
    CUSTOM_SECURITY_MANAGER = SupersetCustomSecurityManager

5. If you wish to have multiple authentication providers, add them to the ``OAUTH_PROVIDERS`` list.

How it works
--------

Being able to authenticate with Okta as a provider and using the ``SupersetCustomSecurityManager`` creates users inside the FlaskApp database and uses the Okta token as a password.

These users are added on first login, and identified in subsequent logins by means of the ``username``.
Once authenticated, the is given a Superset Role that is mapped to the pre-defined Okta groups. This occurs in the ``get_user_role()`` function.

If the user resides in the ``Superset_Admin`` Okta group, it is then given an ``Admin`` role within Superset.
If the user resides in the ``Superset_Explorer`` Okta group, it is then given an ``Alpha`` role within Superset, as well as the ``sql_lab`` role.
All non-mapped users in Okta are given a ``Public`` role. More on Superset roles `here <https://superset.apache.org/docs/security/>`__.
