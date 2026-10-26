import unittest

from hyper_sdk import generate_kasada_user_agent


class KasadaUserAgent(unittest.TestCase):
    def test_matches_documented_vector(self):
        ua = generate_kasada_user_agent("18.0.1", "com.example.app", "9.15.0")
        self.assertEqual(ua, "7016adc4ba8d433533954ebad33be424")


if __name__ == "__main__":
    unittest.main()
