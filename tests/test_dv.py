import unittest

from hyper_sdk import KasadaPayloadInput, generate_kasada_dv, generate_kasada_user_agent


class KasadaDv(unittest.TestCase):
    # A user-agent and dv built from one set of inputs, in the four-field form the i-2.x iOS SDK sends.
    def test_matches_documented_vector(self):
        self.assertEqual(
            generate_kasada_dv("18.0.1", "iPhone13,2", "com.example.app", "9.15.0"),
            "QkZWEmcDRUBEDloaAg8FDhpTAwhEGxFFWRFcQAVCVHFXFAlBUDRRDl8DBgABUxYUGkxERn0HDwNEVFxAFgZAVglAXV0dV0MTG0gbAEEWYVZfEl1XVg8OFA1NHAxIBxFQ",
        )
        self.assertEqual(
            generate_kasada_user_agent("18.0.1", "com.example.app", "9.15.0"),
            "7016adc4ba8d433533954ebad33be424",
        )

    def test_payload_input_sends_dv_only_when_set(self):
        base = ("ua", "https://example.com/ips.js", "script", "en-US", "203.0.113.7")
        self.assertNotIn("dv", KasadaPayloadInput(*base).to_dict())
        self.assertEqual(KasadaPayloadInput(*base, dv="abc").to_dict()["dv"], "abc")


if __name__ == "__main__":
    unittest.main()
