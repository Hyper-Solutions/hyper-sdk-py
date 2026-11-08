"""SEC-CPT challenge parsing and answer generation."""

import base64
import json
import unittest

from hyper_sdk.akamai import SecCptChallenge

CHALLENGE = {
    "token": "tok",
    "timestamp": 1713283747,
    "nonce": "ebccdb479fcb92636fbc",
    "difficulty": 1500,
    "count": 3,
}


class ParseFromJsonTest(unittest.TestCase):
    def test_reads_every_challenge_field(self):
        payload = json.dumps({
            **CHALLENGE,
            "sec-cp-challenge": "true",
            "provider": "adaptive",
            "chlg_duration": 5,
            "branding_url_content": "/_sec/cp_challenge/ak-challenge-4-3.htm",
        })

        challenge = SecCptChallenge.parse_from_json(payload)

        self.assertEqual(challenge.duration, 5)
        self.assertEqual(challenge.challenge_path, "/_sec/cp_challenge/ak-challenge-4-3.htm")
        data = challenge.challenge_data
        self.assertEqual(
            (data.token, data.timestamp, data.nonce, data.difficulty, data.count),
            ("tok", 1713283747, "ebccdb479fcb92636fbc", 1500, 3),
        )

    def test_payload_has_count_answers(self):
        challenge = SecCptChallenge.parse_from_json(json.dumps(CHALLENGE))

        payload = json.loads(challenge.generate_sec_cpt_payload("ABCDEF~3~xyz"))

        self.assertEqual(payload["token"], "tok")
        self.assertEqual(len(payload["answers"]), 3)

    def test_missing_count_yields_no_answers(self):
        challenge = SecCptChallenge.parse_from_json(json.dumps({k: v for k, v in CHALLENGE.items() if k != "count"}))

        payload = json.loads(challenge.generate_sec_cpt_payload("ABCDEF~3~xyz"))

        self.assertEqual(payload["answers"], [])


class ParseHtmlTest(unittest.TestCase):
    def test_html_and_json_parse_to_the_same_challenge_data(self):
        encoded = base64.b64encode(json.dumps(CHALLENGE).encode()).decode()
        html = (
            f'<iframe id="sec-cpt-if" provider="crypto" challenge="{encoded}" '
            f'data-duration=5 src="/_sec/cp_challenge/ak-challenge-4-3.htm"></iframe>'
        )

        from_html = SecCptChallenge.parse(html).challenge_data
        from_json = SecCptChallenge.parse_from_json(json.dumps(CHALLENGE)).challenge_data

        self.assertEqual(vars(from_html), vars(from_json))


if __name__ == "__main__":
    unittest.main()
