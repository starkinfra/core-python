from starkcore.utils.host import StarkHost
import starkcore.utils.rest
from starkcore.utils.resource import Resource
from unittest import TestCase, main
from tests.utils.user import exampleProject
from datetime import datetime, timedelta
from uuid import uuid4
import time


class Transaction(Resource):

    def __init__(self, id, amount):
        Resource.__init__(self, id=id)
        self.amount = amount


class Invoice(Resource):

    def __init__(self, amount, tax_id, name, id=None):
        Resource.__init__(self, id=id)
        self.amount = amount
        self.tax_id=tax_id
        self.name=name


class Webhook(Resource):
    def __init__(self, url, subscriptions, id=None):
        Resource.__init__(self, id=id)

        self.url = url
        self.subscriptions = subscriptions


class TestRestGet(TestCase):

    def test_success_get_page(self):
        transactions, _cursor = starkcore.utils.rest.get_page(
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
        self.assertIsInstance(transaction.amount, int)

    def test_success_get_stream(self):
        transactions = starkcore.utils.rest.get_stream(
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
        for t in transactions:
            self.assertIsInstance(t.amount, int)

    def test_success_get_id(self):
        transactions = starkcore.utils.rest.get_stream(
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
        example_id=""
        for t in transactions:
            example_id = t.id

        transaction = starkcore.utils.rest.get_id(
            id=example_id,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Transaction, "name": "Transaction"},
            language="pt-BR",
            timeout=15,
        )
        self.assertIsInstance(transaction.amount, int)

    def test_success_get_content(self):
        invoices = starkcore.utils.rest.get_stream(
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Invoice, "name": "Invoice"},
            language="pt-BR",
            timeout=15,
            before="2022-02-01",
            limit=1,
        )
        example_id=""
        for i in invoices:
            example_id = i.id

        pdf = starkcore.utils.rest.get_content(
            id=example_id,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Invoice, "name": "Invoice"},
            sub_resource_name="pdf",
            language="pt-BR",
            timeout=15,
        )
        self.assertGreater(len(pdf), 1000)


class TestRestRaw(TestCase):

    def test_success_get(self):
        path = "/invoice"
        query = {
            "limit": 10,
        }
        request = starkcore.utils.rest.get_raw(
            path=path,
            query=query,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )
        self.assertEqual(10, len(request["invoices"]))

    def test_success_post(self):
        path = "/invoice"
        data = {
            "invoices": [{
                "amount": 100,
                "name": "Iron Bank S.A.",
                "taxId": "20.018.183/0001-80"
            }]
        }
        request = starkcore.utils.rest.post_raw(
            path=path,
            payload=data,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )
        self.assertEqual(request["invoices"][0]["amount"], 100)

    def test_success_patch(self):
        initial_state = starkcore.utils.rest.get_raw(
            path=f'/invoice/',
            query={"limit": 1, "status": "paid"},
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )
        example_id = initial_state["invoices"][0]["id"]
        amount = initial_state["invoices"][0]["amount"]

        request = starkcore.utils.rest.patch_raw(
            path=f'/invoice/{example_id}/',
            payload={"amount": amount - amount},
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )

        final_state = starkcore.utils.rest.get_raw(
            path=f'/invoice/{example_id}',
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )
        self.assertEqual(final_state["invoice"]["amount"], 0)

    def test_success_put(self):
        path = "/split-profile"
        data = {
            "profiles": [
                {
                    "interval": "day",
                    "delay": 0
                }
            ]
        }

        request = starkcore.utils.rest.put_raw(
            path=path,
            payload=data,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )

        self.assertEqual(request["profiles"][0]["delay"], 0)
        self.assertEqual(request["profiles"][0]["interval"], "day")

    def test_success_delete(self):
        future_date = datetime.now().date() + timedelta(days=10)

        data = {
            "transfers": [
                {
                    "amount": 10000,
                    "name": "Steve Rogers",
                    "taxId": "330.731.970-10",
                    "bankCode": "001",
                    "branchCode": "1234",
                    "accountNumber": "123456-0",
                    "accountType": "checking",
                    "scheduled": future_date.strftime("%Y-%m-%d"),
                    "externalId": str(int(time.time() * 1000)),
                }
            ]
        }

        create = starkcore.utils.rest.post_raw(
            path="/transfer/",
            payload=data,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="en-US",
            timeout=15,
        )

        request = starkcore.utils.rest.delete_raw(
            path=f'/transfer/{create["transfers"][0]["id"]}',
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="en-US",
            timeout=15,
        )
        try:
            path = f'/invoice/{create["transfers"][0]["id"]}'
            request = starkcore.utils.rest.get_raw(
                path=path,
                sdk_version="0.0.0",
                host=StarkHost.bank,
                api_version="v2",
                user=exampleProject,
                language="pt-BR",
                timeout=15,
            )
        except Exception as e:
            err = str(e.errors[0]).split(":")[0]
            self.assertEqual("invalidInvoice", err)
        if "transfers" in request:
            raise Exception


class TestRestPost(TestCase):

    def test_success_post_multi(self):
        invoice = Invoice(amount=100, tax_id="012.345.678-90", name="Arya Stark")
        request = starkcore.utils.rest.post_multi(
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Invoice, "name": "Invoice"},
            entities=[invoice],
            language="pt-BR",
            timeout=15,
        )
        for i in request:
            self.assertIsInstance(i, Invoice)

    def test_success_post_single_and_delete_id(self):
        webhook = Webhook(
            url="https://webhook.site/{uuid}".format(uuid=str(uuid4())),
            subscriptions=["transfer", "boleto-payment"]
        )
        create = starkcore.utils.rest.post_single(
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Webhook, "name": "Webhook"},
            entity=webhook,
            language="pt-BR",
            timeout=15,
        )
        self.assertIsInstance(create, Webhook)
        delete = starkcore.utils.rest.delete_id(
            id=create.id,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Webhook, "name": "Webhook"},
            entity=webhook,
            language="pt-BR",
            timeout=15,
        )
        confirm = ""
        try:
            confirm = starkcore.utils.rest.get_id(
                id=create.id,
                sdk_version="0.0.0",
                host=StarkHost.bank,
                api_version="v2",
                user=exampleProject,
                resource={"class": Webhook, "name": "Webhook"},
                language="pt-BR",
                timeout=15,
            )
        except Exception as e:
            err = str(e.errors[0]).split(":")[0]
            self.assertEqual("invalidWebhookId", err)
            pass
        print(confirm)
        if isinstance(confirm, Webhook):
            raise Exception


class TestRestPatch(TestCase):

    def test_success_patch_id(self):
        invoices = starkcore.utils.rest.get_stream(
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            resource={"class": Invoice, "name": "Invoice"},
            status="paid",
            language="pt-BR",
            timeout=15,
            before="2022-02-01",
            limit=1,
        )
        example_id = ""
        for i in invoices:
            example_id = i.id
        body = {"amount": 0}
        invoice = starkcore.utils.rest.patch_id(
            id=example_id,
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            payload=body,
            resource={"class": Invoice, "name": "Invoice"},
            language="pt-BR",
            timeout=15,
        )
        self.assertEqual(invoice.amount, 0)


if __name__ == '__main__':
    main()
