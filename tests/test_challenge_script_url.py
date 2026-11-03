"""Finds the deferred DataDome challenge bundle on a device check or captcha page."""

import unittest

from hyper_sdk.datadome import parse_challenge_script_url


class TestParseChallengeScriptUrl(unittest.TestCase):
    def test_interstitial_with_build(self):
        html = '<head><script defer src="https://ct.captcha-delivery.com/interstitial.1.33.0.202609141.js"></script></head>'
        self.assertEqual(parse_challenge_script_url(html), "https://ct.captcha-delivery.com/interstitial.1.33.0.202609141.js")

    def test_captcha_with_build(self):
        html = '<script defer src="https://ct.captcha-delivery.com/captcha.1.34.0.202609141.js"></script>'
        self.assertEqual(parse_challenge_script_url(html), "https://ct.captcha-delivery.com/captcha.1.34.0.202609141.js")

    def test_interstitial_without_build(self):
        html = '<head><script defer src="https://ct.captcha-delivery.com/interstitial.1.36.0.js"></script></head>'
        self.assertEqual(parse_challenge_script_url(html), "https://ct.captcha-delivery.com/interstitial.1.36.0.js")

    def test_single_quotes(self):
        html = "<script src='https://ct.captcha-delivery.com/captcha.1.37.0.js'></script>"
        self.assertEqual(parse_challenge_script_url(html), "https://ct.captcha-delivery.com/captcha.1.37.0.js")

    def test_versionless_loader(self):
        html = '<script src="https://ct.captcha-delivery.com/i.js"></script>'
        self.assertIsNone(parse_challenge_script_url(html))

    def test_inlined_bundle(self):
        html = "<script>var ddm = {};/* DataDome is a cyberfraud solution v1.33.0 */!function(){}()</script>"
        self.assertIsNone(parse_challenge_script_url(html))


if __name__ == "__main__":
    unittest.main()
