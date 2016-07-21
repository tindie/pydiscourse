"""
Utilities to implement Single Sign On for Discourse with a Python managed
authentication DB

https://meta.discourse.org/t/official-single-sign-on-for-discourse/13045

Thanks to James Potter for the heavy lifting, detailed at
https://meta.discourse.org/t/sso-example-for-django/14258

A SSO request handler might look something like

    @login_required
    def discourse_sso_view(request):
        payload = request.GET.get('sso')
        signature = request.GET.get('sig')
        try:
            nonce = sso_validate(payload, signature, SECRET)
        except DiscourseError as e:
            return HTTP400(e.args[0])

        url = sso_redirect_url(nonce, SECRET, request.user.email,
                request.user.id, request.user.username)
        return redirect('http://discuss.example.com' + url)
"""
from base64 import b64encode, b64decode
import hmac
import hashlib

try:  # py3
    from urllib.parse import unquote, urlencode, parse_qs
except ImportError:
    from urllib import unquote, urlencode
    from urlparse import parse_qs


from pydiscourse.exceptions import DiscourseError


def sso_validate(payload, signature, secret):
    """
        payload: provided by Discourse HTTP call to your SSO endpoint as sso GET param
        signature: provided by Discourse HTTP call to your SSO endpoint as sig GET param
        secret: the secret key you entered into Discourse sso secret

        return value: The nonce used by discourse to validate the redirect URL
    """
    if None in [payload, signature]:
        raise DiscourseError('No SSO payload or signature.')

    if not secret:
        raise DiscourseError('Invalid secret..')

    payload = unquote(payload)
    if not payload:
        raise DiscourseError('Invalid payload..')

    decoded = b64decode(payload.encode('utf-8')).decode('utf-8')
    if 'nonce' not in decoded:
        raise DiscourseError('Invalid payload..')

    h = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        raise DiscourseError('Payload does not match signature.')

    # Discourse returns querystring encoded value. We only need `nonce`
    qs = parse_qs(decoded)
    return qs['nonce'][0]


def sso_payload(secret, **kwargs):
    return_payload = b64encode(urlencode(kwargs).encode('utf-8'))
    h = hmac.new(secret.encode('utf-8'), return_payload, digestmod=hashlib.sha256)
    query_string = urlencode({'sso': return_payload, 'sig': h.hexdigest()})
    return query_string


def sso_redirect_url(nonce, secret, email, external_id, username, **kwargs):
    """
        nonce: returned by sso_validate()
        secret: the secret key you entered into Discourse sso secret
        user_email: email address of the user who logged in
        user_id: the internal id of the logged in user
        user_username: username of the logged in user

        return value: URL to redirect users back to discourse, now logged in as user_username
    """
    kwargs.update({
        'nonce': nonce,
        'email': email,
        'external_id': external_id,
        'username': username
    })

    return '/session/sso_login?%s' % sso_payload(secret, **kwargs)
