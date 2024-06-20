from time import time
from json import dumps, loads
from ellipticcurve import Ecdsa
from sys import version_info as python_version
from ..environment import Environment
from ..error import InternalServerError, InputErrors, UnknownError
from .host import StarkHost
from .url import urlencode
from .checks import check_user, check_language
from ..user.__publicuser import PublicUser


class Response:

    def __init__(self, status, content, headers):
        self.status = status
        self.content = content
        self.headers = headers

    def json(self):
        return loads(self.content.decode("utf-8"))


def fetch(host, sdk_version, user, method, path, payload=None, query=None,
          prefix="", api_version="v2", language="en-US", timeout=15, raiseException=True):
    user = check_user(user)
    language = check_language(language)

    service = {
        StarkHost.infra: "starkinfra",
        StarkHost.bank: "starkbank",
        StarkHost.sign: "starksign",
    }[host]

    url = {
        Environment.production:  "https://api.{service}.com/",
        Environment.sandbox:     "https://sandbox.api.{service}.com/",
    }[user.environment].format(service=service) + api_version

    url = "{base_url}/{path}{query}".format(base_url=url, path=path, query=urlencode(query))

    agent = "{prefix}Python-{major}.{minor}.{micro}-SDK-{host}-{sdk_version}".format(
        prefix=prefix + "-" if prefix else "",
        major=python_version.major,
        minor=python_version.minor,
        micro=python_version.micro,
        host=host,
        sdk_version=sdk_version,
    )

    body = dumps(payload) if payload else ""
    headers = {
        "User-Agent": agent,
        "Accept-Language": language,
        "Content-Type": "application/json",
    }
    headers.update(_authentication_headers(user=user, body=body))
    try:
        request = method(
            url=url,
            data=body,
            headers=headers,
            timeout=timeout,
        )
        response = Response(status=request.status_code, content=request.content, headers=request.headers)
    except Exception as exception:
        error = "{}: {}".format(exception.__class__.__name__, str(exception.__context__))
        response = Response(status=0, content=error, headers={})

    if not raiseException:
        return response

    if response.status == 500:
        raise InternalServerError()
    if response.status == 400:
        raise InputErrors(response.json()["errors"])
    if response.status != 200:
        raise UnknownError(response.content)
    return response


def _authentication_headers(user, body):
    if isinstance(user, PublicUser):
        return {}

    access_time = str(time())
    message = "{access_id}:{access_time}:{body}".format(access_id=user.access_id(), access_time=access_time, body=body)
    signature = Ecdsa.sign(message=message, privateKey=user.private_key()).toBase64()

    return {
        "Access-Id": user.access_id(),
        "Access-Time": access_time,
        "Access-Signature": signature,
    }
