"""Runs the real Session / SessionAsync methods against canned API responses."""

import asyncio
import json
import unittest

import httpx

from hyper_sdk import (
    Session, SessionAsync, SensorInput, SbsdInput, ReeseInput, KasadaPayloadInput,
    DataDomeSliderInput, DataDomeInterstitialInput, DataDomeTagsInput,
)

HINTS = {
    "sec-ch-ua": '"Chromium";v="154"',
    "sec-ch-prefers-color-scheme": "dark",
    "rtt": "150",
}
BODY = {"payload": "p", "context": "c", "headers": HINTS}
KASADA_BODY = {
    "payload": "dGwtYm9keQ==",
    "headers": {"x-kpsdk-ct": "ct", "x-kpsdk-v": "j-1.0.0"},
    "clientHints": {"rtt": "100", "sec-ch-ua-wow64": "?0"},
}


def recorder(body):
    """A MockTransport handler that answers with body and records request bodies."""
    sent = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json=body)

    return handler, sent


def sensor_input():
    return SensorInput(abck="", bmsz="", version="3", page_url="", user_agent="", ip="",
                       accept_language="", context="", script="", script_url="")


def sbsd_input(script_url=""):
    return SbsdInput(user_agent="", uuid="", page_url="", o_cookie="", script="",
                     accept_language="", ip="", script_url=script_url)


def kasada_input(strict=False):
    return KasadaPayloadInput(user_agent="", ips_link="", script="", accept_language="", ip="",
                              strict=strict)


def slider_input():
    return DataDomeSliderInput(user_agent="", device_link="", html="", puzzle="", piece="", parent_url="",
                               accept_language="", ip="")


def interstitial_input():
    return DataDomeInterstitialInput(user_agent="", device_link="", html="", accept_language="", ip="")


def tags_input():
    return DataDomeTagsInput(user_agent="", ddk="", referer="", tags_type="", version="", accept_language="", ip="")


def reese_input():
    return ReeseInput(user_agent="", accept_language="", ip="", script_url="", pageUrl="", pow="", script="")


class SyncResults(unittest.TestCase):
    def session(self, body):
        handler, sent = recorder(body)
        return Session("test-key", client=httpx.Client(transport=httpx.MockTransport(handler))), sent

    def test_client_hints_reach_every_result(self):
        s, _ = self.session(BODY)
        sensor = s.generate_sensor_data(sensor_input())
        self.assertEqual((sensor.payload, sensor.context, sensor.client_hints), ("p", "c", HINTS))
        sbsd = s.generate_sbsd_data(sbsd_input())
        self.assertEqual((sbsd.payload, sbsd.context, sbsd.client_hints), ("p", "c", HINTS))
        self.assertEqual(s.generate_reese84_sensor(reese_input()).client_hints, HINTS)
        self.assertEqual(s.generate_slider_payload(slider_input()).client_hints, HINTS)
        self.assertEqual(s.generate_interstitial_payload(interstitial_input()).client_hints, HINTS)
        self.assertEqual(s.generate_tags_payload(tags_input()).client_hints, HINTS)

    def test_kasada_keeps_kpsdk_headers_apart_from_client_hints(self):
        s, _ = self.session(KASADA_BODY)
        res = s.generate_kasada_payload(kasada_input())
        self.assertEqual(res.payload, "dGwtYm9keQ==")
        self.assertEqual(res.headers, {"x-kpsdk-ct": "ct", "x-kpsdk-v": "j-1.0.0"})
        self.assertEqual(res.client_hints, {"rtt": "100", "sec-ch-ua-wow64": "?0"})

    def test_missing_client_hints_are_none(self):
        s, _ = self.session({"payload": "p"})
        self.assertIsNone(s.generate_reese84_sensor(reese_input()).client_hints)

    def test_strict_and_script_url_only_sent_when_set(self):
        s, sent = self.session(dict(KASADA_BODY, context="c"))
        s.generate_kasada_payload(kasada_input())
        s.generate_kasada_payload(kasada_input(strict=True))
        s.generate_sbsd_data(sbsd_input())
        s.generate_sbsd_data(sbsd_input(script_url="https://example.com/abc.js?v=1"))
        self.assertNotIn("strict", sent[0])
        self.assertIs(sent[1]["strict"], True)
        self.assertNotIn("scriptUrl", sent[2])
        self.assertEqual(sent[3]["scriptUrl"], "https://example.com/abc.js?v=1")

    def test_api_error_still_raises(self):
        s, _ = self.session({"error": "boom"})
        with self.assertRaises(Exception):
            s.generate_sensor_data(sensor_input())


class AsyncResults(unittest.TestCase):
    def run_async(self, body, call):
        handler, sent = recorder(body)

        async def go():
            client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
            async with SessionAsync("test-key", client=client) as s:
                res = await call(s)
            await client.aclose()
            return res

        return asyncio.run(go()), sent

    def test_client_hints_reach_the_result(self):
        res, _ = self.run_async(BODY, lambda s: s.generate_sensor_data(sensor_input()))
        self.assertEqual((res.payload, res.context, res.client_hints), ("p", "c", HINTS))
        res, _ = self.run_async(BODY, lambda s: s.generate_tags_payload(tags_input()))
        self.assertEqual(res.client_hints, HINTS)

    def test_kasada_payload_and_strict(self):
        res, sent = self.run_async(KASADA_BODY, lambda s: s.generate_kasada_payload(kasada_input(strict=True)))
        self.assertEqual(res.headers["x-kpsdk-ct"], "ct")
        self.assertEqual(res.client_hints["rtt"], "100")
        self.assertIs(sent[0]["strict"], True)


if __name__ == "__main__":
    unittest.main()
