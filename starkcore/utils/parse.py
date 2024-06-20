from json import loads, dumps
from ellipticcurve import Ecdsa, PublicKey, Signature
from ..utils.cache import cache
from ..utils.api import from_api_json
from ..error import InvalidSignatureError
from .rest import get_raw


def parse_and_verify(content, signature, sdk_version, api_version, host, resource, user, language, timeout, key=None):
    content = verify(content, signature, sdk_version, api_version, host, user, language, timeout)
    json = loads(content, strict=False)
    if key:
        json = json[key]
    return from_api_json(resource=resource, json=json)


def verify(content, signature, sdk_version, api_version, host, user, language, timeout):
    try:
        signature = Signature.fromBase64(signature)
    except:
        raise InvalidSignatureError("The provided signature is not valid")

    public_key = _get_public_key(
        sdk_version=sdk_version,
        host=host,
        api_version=api_version,
        user=user,
        language=language,
        timeout=timeout,
    )
    if _is_signature_valid(content=content, signature=signature, public_key=public_key):
        return content

    public_key = _get_public_key(
        sdk_version=sdk_version,
        host=host,
        api_version=api_version,
        user=user,
        language=language,
        timeout=timeout,
        refresh=True,
    )
    if _is_signature_valid(content=content, signature=signature, public_key=public_key):
        return content

    raise InvalidSignatureError("The provided signature and content do not match the public key")


def _is_signature_valid(content, signature, public_key):
    if Ecdsa.verify(message=content, signature=signature, publicKey=public_key):
        return True

    try:
        normalized = dumps(loads(content), sort_keys=True)
    except:
        return False

    if Ecdsa.verify(message=normalized, signature=signature, publicKey=public_key):
       return True
    return False


def _get_public_key(sdk_version, host, api_version, user, language, timeout, refresh=False):
    public_key = cache.get("starkcore-public-key")
    if public_key and not refresh:
        return public_key

    pem = get_raw(
        sdk_version=sdk_version,
        host=host,
        api_version=api_version,
        path="/public-key",
        user=user,
        language=language,
        timeout=timeout,
        query={"limit": 1}
    ).json()["publicKeys"][0]["content"]
    public_key = PublicKey.fromPem(pem)
    cache["stark-public-key"] = public_key
    return public_key
