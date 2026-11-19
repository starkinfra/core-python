from json import dumps, loads
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from ellipticcurve import PrivateKey
import starkcore.utils.rest
from starkcore import Project
from starkcore.error import InputErrors
from starkcore.utils.host import StarkHost
from starkcore.utils.resource import Resource


class Card(Resource):

    def __init__(self, id=None, holder_name=None, holder_tax_id=None, holder_external_id=None, tags=None):
        Resource.__init__(self, id=id)
        self.holder_name = holder_name
        self.holder_tax_id = holder_tax_id
        self.holder_external_id = holder_external_id
        self.tags = tags


exampleUser = Project(
    environment="sandbox",
    id="5656565656565656",
    private_key=PrivateKey().toPem(),
)


def fakeHttpResponse(status, body):
    response = MagicMock()
    response.status_code = status
    response.content = dumps(body).encode("utf-8")
    response.headers = {}
    return response


def patchMultiCards(entities, **query):
    return starkcore.utils.rest.patch_multi(
        sdk_version="0.0.0",
        host=StarkHost.infra,
        api_version="v2",
        user=exampleUser,
        resource={"class": Card, "name": "Card"},
        entities=entities,
        language="en-US",
        timeout=15,
        **query
    )


# Only the outgoing HTTP call (requests.patch) is replaced: signing, headers and payload building run for real.
class TestPatchMulti(TestCase):

    def test_success_sends_patch_with_plural_payload_and_parses_response(self):
        apiCards = [
            {"id": "1", "holderName": "Tony Stark", "holderTaxId": "012.345.678-90", "holderExternalId": "a", "tags": []},
            {"id": "2", "holderName": "Tony Stark", "holderTaxId": "012.345.678-90", "holderExternalId": "a", "tags": []},
        ]
        with patch("starkcore.utils.rest.patch", return_value=fakeHttpResponse(200, {"cards": apiCards})) as sent:
            cards = patchMultiCards([
                Card(id="1", holder_name="Tony Stark", holder_tax_id="012.345.678-90", holder_external_id="a"),
                {"id": "2", "holder_name": "Tony Stark", "holder_tax_id": "012.345.678-90", "holder_external_id": "a"},
            ])
        sent.assert_called_once()
        call = sent.call_args.kwargs
        self.assertTrue(call["url"].endswith("/v2/card"))
        self.assertEqual(call["headers"]["Content-Type"], "application/json")
        self.assertIn("Access-Signature", call["headers"])
        self.assertEqual(loads(call["data"]), {"cards": [
            {"id": "1", "holderName": "Tony Stark", "holderTaxId": "012.345.678-90", "holderExternalId": "a"},
            {"id": "2", "holderName": "Tony Stark", "holderTaxId": "012.345.678-90", "holderExternalId": "a"},
        ]})
        self.assertEqual([card.id for card in cards], ["1", "2"])
        self.assertTrue(all(isinstance(card, Card) for card in cards))
        self.assertEqual(cards[0].holder_name, "Tony Stark")

    def test_unset_attributes_are_not_sent(self):
        with patch("starkcore.utils.rest.patch", return_value=fakeHttpResponse(200, {"cards": [{"id": "1"}]})) as sent:
            patchMultiCards([Card(id="1", tags=["x"])])
        self.assertEqual(loads(sent.call_args.kwargs["data"]), {"cards": [{"id": "1", "tags": ["x"]}]})

    def test_query_parameters_are_sent_in_the_url(self):
        with patch("starkcore.utils.rest.patch", return_value=fakeHttpResponse(200, {"cards": [{"id": "1"}]})) as sent:
            patchMultiCards([Card(id="1")], expand=["rules"])
        self.assertTrue(sent.call_args.kwargs["url"].endswith("/v2/card?expand=rules"))

    def test_api_error_is_raised_untouched(self):
        errors = [{"code": "invalidHolder", "message": "Element 0: must all be provided together, or none at all."}]
        with patch("starkcore.utils.rest.patch", return_value=fakeHttpResponse(400, {"errors": errors})):
            with self.assertRaises(InputErrors) as context:
                patchMultiCards([Card(id="1", holder_name="Tony Stark")])
        self.assertEqual([error.code for error in context.exception.errors], ["invalidHolder"])


if __name__ == "__main__":
    main()
