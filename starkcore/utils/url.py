from .case import snake_to_camel
from .api import cast_json_to_api_format
from .compatibility import urlencode as _urlencode


def urlencode(params):
    params = cast_json_to_api_format(params) if params else {}
    if "expand" in params:
        params["expand"] = [snake_to_camel(value) for value in params["expand"]]
    params = {k: valueToString(v) for k, v in params.items()}
    return "?" + _urlencode(params) if params else ""


def valueToString(value):
    if isinstance(value, (tuple, list, set)):
        return ",".join([valueToString(value) for value in value])
    return str(value)
