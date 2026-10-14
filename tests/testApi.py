from starkcore.utils.api import last_name_plural
from unittest import TestCase, main


class TestApi(TestCase):

    def test_plural_of_name_ending_in_ch(self):
        self.assertEqual("speeches", last_name_plural({"name": "AiSpeech"}))

    def test_plural_of_name_ending_in_sh(self):
        self.assertEqual("dashes", last_name_plural({"name": "Dash"}))

    def test_plural_of_name_ending_in_x(self):
        self.assertEqual("taxes", last_name_plural({"name": "Tax"}))

    def test_plural_of_regular_name(self):
        self.assertEqual("logs", last_name_plural({"name": "Log"}))

    def test_plural_of_name_ending_in_y(self):
        self.assertEqual("entities", last_name_plural({"name": "Entity"}))

    def test_plural_of_name_ending_in_ey(self):
        self.assertEqual("keys", last_name_plural({"name": "Key"}))

    def test_plural_of_name_ending_in_s_is_unchanged(self):
        self.assertEqual("address", last_name_plural({"name": "Address"}))

    def test_plural_uses_only_the_last_word(self):
        self.assertEqual("speeches", last_name_plural({"name": "AiVoiceSpeech"}))


if __name__ == '__main__':
    main()
