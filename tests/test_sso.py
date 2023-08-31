from base64 import b64decode
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs

import pytest

from pydiscourse import sso
from pydiscourse.exceptions import DiscourseError


def test_sso_validate_missing_payload():
    with pytest.raises(DiscourseError) as excinfo:
        sso.sso_validate(None, "abc", "123")

    assert excinfo.value.args[0] == "No SSO payload or signature."


def test_sso_validate_empty_payload():
    with pytest.raises(DiscourseError) as excinfo:
        sso.sso_validate("", "abc", "123")

    assert excinfo.value.args[0] == "Invalid payload."


def test_sso_validate_missing_signature():
    with pytest.raises(DiscourseError) as excinfo:
        sso.sso_validate("sig", None, "123")

    assert excinfo.value.args[0] == "No SSO payload or signature."


@pytest.mark.parametrize("bad_secret", [None, ""])
def test_sso_validate_missing_secret(bad_secret):
    with pytest.raises(DiscourseError) as excinfo:
        sso.sso_validate("payload", "signature", bad_secret)

    assert excinfo.value.args[0] == "Invalid secret."


def test_sso_validate_invalid_signature(sso_payload, sso_signature, sso_secret):
    with pytest.raises(DiscourseError) as excinfo:
        sso.sso_validate("Ym9i", sso_signature, sso_secret)

    assert excinfo.value.args[0] == "Invalid payload."


def test_sso_validate_invalid_payload_nonce(sso_payload, sso_secret):
    with pytest.raises(DiscourseError) as excinfo:
        sso.sso_validate(sso_payload, "notavalidsignature", sso_secret)

    assert excinfo.value.args[0] == "Payload does not match signature."


def test_valid_nonce(sso_payload, sso_signature, sso_secret, sso_nonce):
    generated_nonce = sso.sso_validate(sso_payload, sso_signature, sso_secret)
    assert generated_nonce == sso_nonce


def test_valid_redirect_url(
    sso_secret,
    sso_nonce,
    name,
    email,
    username,
    external_id,
    redirect_url,
):
    url = sso.sso_redirect_url(
        sso_nonce,
        sso_secret,
        email,
        external_id,
        username,
        name="sam",
    )

    assert "/session/sso_login" in url[:20]

    # check its valid, using our own handy validator
    params = parse_qs(urlparse(url).query)
    payload = params["sso"][0]
    sso.sso_validate(payload, params["sig"][0], sso_secret)

    # check the params have all the data we expect
    payload = b64decode(payload.encode("utf-8")).decode("utf-8")
    payload = unquote(payload)
    payload = dict(p.split("=") for p in payload.split("&"))

    assert payload == {
        "username": username,
        "nonce": sso_nonce,
        "external_id": external_id,
        "name": name,
        "email": email,
    }
