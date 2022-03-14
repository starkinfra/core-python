from starkcore.utils.host import StarkHost
from starkcore.utils.rest import get_page
from starkcore.utils.resource import Resource
from unittest import TestCase, main
from tests.utils.user import exampleProject


class Transaction(Resource):

    def __init__(self, id, amount):
        Resource.__init__(self, id=id)
        self.amount = amount


class TestRestGet(TestCase):

    def test_success(self):
        transactions, _cursor = get_page(
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Transaction, "name": "Transaction"},
            language="pt-BR",
            timeout=15,
            before="2022-02-01",
            limit=1,
        )
        transaction = transactions[0]
        print(transaction)
        self.assertIsInstance(transaction.amount, int)


if __name__ == '__main__':
    main()
