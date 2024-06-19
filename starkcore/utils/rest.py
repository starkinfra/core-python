from requests import get, post, delete, patch, put
from ..utils.request import fetch
from ..utils.api import endpoint, last_name, last_name_plural, api_json, from_api_json, cast_json_to_api_format


def get_page(sdk_version, host, api_version, user, resource, language, timeout, **query):
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=get,
        path=endpoint(resource),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entities = [from_api_json(resource, entity) for entity in json[last_name_plural(resource)]]
    cursor = json.get("cursor")
    return entities, cursor


def get_stream(sdk_version, host, api_version, user, resource, language, timeout, limit=None, **query):
    limit_query = {"limit": min(limit, 100) if limit else limit}
    limit_query.update(query)

    while True:
        entities, cursor = get_page(
            host=host,
            sdk_version=sdk_version,
            user=user,
            resource=resource,
            api_version=api_version,
            language=language,
            timeout=timeout,
            **limit_query
        )
        for entity in entities:
            yield entity

        if limit:
            limit -= 100
            limit_query["limit"] = min(limit, 100)

        limit_query["cursor"] = cursor
        if not cursor or (limit is not None and limit <= 0):
            break


def get_id(sdk_version, host, api_version, user, resource, id, language, timeout, **query):
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=get,
        path="{endpoint}/{id}".format(endpoint=endpoint(resource), id=id),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entity = json[last_name(resource)]
    return from_api_json(resource, entity)


def get_content(sdk_version, host, api_version, user, resource, id, sub_resource_name, language, timeout, **query):
    return fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=get,
        path="{endpoint}/{id}/{sub_resource_name}".format(
            endpoint=endpoint(resource),
            id=id,
            sub_resource_name=sub_resource_name,
        ),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).content


def get_sub_resource(sdk_version, host, api_version, user, resource, id, sub_resource, language, timeout, **query):
    entity = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=get,
        path="{endpoint}/{id}/{sub_resource}".format(
            endpoint=endpoint(resource),
            id=id,
            sub_resource=endpoint(sub_resource),
        ),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()[last_name(sub_resource)]
    return from_api_json(sub_resource, entity)


def get_sub_resources(sdk_version, host, api_version, user, resource, id, sub_resource, language, timeout, **query):
    entities = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=get,
        path="{endpoint}/{id}/{sub_resource}".format(
            endpoint=endpoint(resource),
            id=id,
            sub_resource=endpoint(sub_resource),
        ),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()[last_name_plural(sub_resource)]
    return [from_api_json(sub_resource, entity) for entity in entities]


def post_multi(sdk_version, host, api_version, user, resource, entities, language, timeout, **query):
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=post,
        path=endpoint(resource),
        payload={last_name_plural(resource): [api_json(entity) for entity in entities]},
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entities = json[last_name_plural(resource)]
    return [from_api_json(resource, entity) for entity in entities]


def post_single(sdk_version, host, api_version, user, resource, entity, language, timeout, **query):
    payload = api_json(entity)
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=post,
        path=endpoint(resource),
        payload=payload,
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entity_json = json[last_name(resource)]
    return from_api_json(resource, entity_json)


def post_sub_resource(sdk_version, host, api_version, user, resource, id, sub_resource, entity, language, timeout):
    payload = api_json(entity)
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=post,
        path="{endpoint}/{id}/{sub_resource}".format(
            endpoint=endpoint(resource),
            id=id,
            sub_resource=endpoint(sub_resource),
        ),
        payload=payload,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entity_json = json[last_name(sub_resource)]
    return from_api_json(sub_resource, entity_json)


def delete_id(sdk_version, host, api_version, user, resource, id, language, timeout, **query):
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=delete,
        path="{endpoint}/{id}".format(endpoint=endpoint(resource), id=id),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entity = json[last_name(resource)]
    return from_api_json(resource, entity)


def patch_id(sdk_version, host, api_version, user, resource, id, payload, language, timeout, **query):
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=patch,
        path="{endpoint}/{id}".format(endpoint=endpoint(resource), id=id),
        payload=cast_json_to_api_format(payload),
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entity = json[last_name(resource)]
    return from_api_json(resource, entity)


def put_multi(sdk_version, host, api_version, user, resource, entities, language, timeout, **query):
    json = fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=put,
        path=endpoint(resource),
        payload={last_name_plural(resource): [api_json(entity) for entity in entities]},
        query=query,
        api_version=api_version,
        language=language,
        timeout=timeout,
    ).json()
    entities = json[last_name_plural(resource)]
    return [from_api_json(resource, entity) for entity in entities]


def get_raw(sdk_version, host, api_version, path, user, language, timeout, prefix=None, raiseException=True,
            query=None):
    return fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=get,
        path=path,
        query=query,
        api_version=api_version,
        prefix=prefix,
        language=language,
        timeout=timeout,
        raiseException=raiseException,
    )


def post_raw(sdk_version, host, api_version, path, payload, user, language, timeout, prefix=None, raiseException=True,
             query=None):
    return fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=post,
        path=path,
        payload=payload,
        query=query,
        api_version=api_version,
        prefix=prefix,
        language=language,
        timeout=timeout,
        raiseException=raiseException,
    )


def patch_raw(sdk_version, host, api_version, path, payload, user, language, timeout, prefix=None, raiseException=True,
              query=None):
    return fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=patch,
        path=path,
        payload=payload,
        query=query,
        api_version=api_version,
        prefix=prefix,
        language=language,
        timeout=timeout,
        raiseException=raiseException,
    )


def put_raw(sdk_version, host, api_version, path, payload, user, language, timeout, prefix=None, raiseException=True,
            query=None):
    return fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=put,
        path=path,
        payload=payload,
        query=query,
        api_version=api_version,
        prefix=prefix,
        language=language,
        timeout=timeout,
        raiseException=raiseException,
    )


def delete_raw(sdk_version, host, api_version, path, user, language, timeout, prefix=None, payload=None,
               raiseException=True, query=None):
    return fetch(
        host=host,
        sdk_version=sdk_version,
        user=user,
        method=delete,
        path=path,
        payload=payload,
        query=query,
        api_version=api_version,
        prefix=prefix,
        language=language,
        timeout=timeout,
        raiseException=raiseException,
    )
