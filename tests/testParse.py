import starkcore.utils.parse
from starkcore.utils.host import StarkHost
from tests.utils.user import exampleProject
from ellipticcurve import PublicKey
from unittest import TestCase, main


class TestParse(TestCase):

    def test_get_public_key(self):
        request = starkcore.utils.parse._get_public_key(
            sdk_version="0.0.0",
            host=StarkHost.bank,
            api_version="v2",
            user=exampleProject,
            language="pt-BR",
            timeout=15,
        )
        self.assertIsInstance(request, PublicKey)


if __name__ == '__main__':
    main()
