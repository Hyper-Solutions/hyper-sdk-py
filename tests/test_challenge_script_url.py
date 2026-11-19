"""Finds the deferred DataDome challenge bundle on a device check or captcha page."""

import unittest

from hyper_sdk.datadome import parse_challenge_script_url

BUILD_PREFIX_URL = "https://ct.captcha-delivery.com/captcha.build623.01-c-v1.38.0-2026-11-17-05h07.js"


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
        html = "<script defer src='https://ct.captcha-delivery.com/captcha.1.37.0.js'></script>"
        self.assertEqual(parse_challenge_script_url(html), "https://ct.captcha-delivery.com/captcha.1.37.0.js")

    def test_captcha_with_build_prefix(self):
        html = f'<script defer src="{BUILD_PREFIX_URL}"></script>'
        self.assertEqual(parse_challenge_script_url(html), BUILD_PREFIX_URL)

    def test_build_prefix_after_inline_dd_object(self):
        html = (
            "<script data-cfasync=\"false\">var dd={'rt':'c'}</script>"
            '<script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script>'
            f'<script defer src="{BUILD_PREFIX_URL}"></script>'
        )
        self.assertEqual(parse_challenge_script_url(html), BUILD_PREFIX_URL)

    def test_any_file_name(self):
        html = '<script defer src="https://ct.captcha-delivery.com/interstitial-next.js"></script>'
        self.assertEqual(parse_challenge_script_url(html), "https://ct.captcha-delivery.com/interstitial-next.js")

    def test_defer_after_src(self):
        html = f'<script src="{BUILD_PREFIX_URL}" defer></script>'
        self.assertEqual(parse_challenge_script_url(html), BUILD_PREFIX_URL)

    def test_first_deferred_tag_wins(self):
        html = (
            f'<script defer src="{BUILD_PREFIX_URL}"></script>'
            '<script defer src="https://example.com/other.js"></script>'
        )
        self.assertEqual(parse_challenge_script_url(html), BUILD_PREFIX_URL)

    def test_defer_in_src_is_not_the_attribute(self):
        html = '<script src="https://example.com/defer.js"></script>'
        self.assertIsNone(parse_challenge_script_url(html))

    def test_versionless_loader(self):
        html = '<script src="https://ct.captcha-delivery.com/i.js"></script>'
        self.assertIsNone(parse_challenge_script_url(html))

    def test_inlined_bundle(self):
        html = "<script>var ddm = {};/* DataDome is a cyberfraud solution v1.33.0 */!function(){}()</script>"
        self.assertIsNone(parse_challenge_script_url(html))


if __name__ == "__main__":
    unittest.main()
