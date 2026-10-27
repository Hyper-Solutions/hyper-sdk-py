"""Sends challenge scripts by hash, falling back to the script when the API has not seen the hash."""

import asyncio
import copy
import hashlib
import json
import unittest

import httpx

from hyper_sdk import (
    Session, SessionAsync, SensorInput, SbsdInput, TelemetryInput, TelemetryParamsInput, ReeseInput, DataDomeSliderInput, DataDomeInterstitialInput,
)

SCRIPT = "(function(){var a='é';return a})();"
SCRIPT_HASH = hashlib.sha256(SCRIPT.encode("utf-8")).hexdigest()
OK = {"payload": "p", "context": "c"}


class FakeAPI:
    """A MockTransport handler that knows the scripts it was sent, the way the API stores them by hash."""

    def __init__(self, known=(), after_script=None):
        self.known = set(known)
        # after_script, when set, is the (status, body) answered to a request that carries the script
        self.after_script = after_script
        self.sent = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        self.sent.append(body)
        if "script" in body and "scriptHash" in body:
            return httpx.Response(400, json={"error": "script and scriptHash are mutually exclusive"})
        if body.get("script"):
            self.known.add(hashlib.sha256(body["script"].encode("utf-8")).hexdigest())
            if self.after_script is not None:
                status, answer = self.after_script
                return httpx.Response(status, json=answer)
        elif "scriptHash" in body and body["scriptHash"] not in self.known:
            return httpx.Response(422, json={"error": "script_required"})
        return httpx.Response(200, json=OK)


def sensor_input(script=SCRIPT, context=""):
    return SensorInput(abck="abck", bmsz="bmsz", version="3", page_url="https://example.com/", user_agent="ua",
                       ip="1.2.3.4", accept_language="en-US", context=context, script=script,
                       script_url="https://example.com/s.js")


def sbsd_input(script=SCRIPT, context=""):
    return SbsdInput(user_agent="ua", uuid="uuid", page_url="https://example.com/", o_cookie="o", script=script,
                     accept_language="en-US", ip="1.2.3.4", context=context)


def telemetry_input(script=SCRIPT):
    return TelemetryInput(abck="abck", bmsz="bmsz", page_url="https://example.com/", user_agent="ua", ip="1.2.3.4",
                          accept_language="en-US", context="", script=script, script_url="https://example.com/s.js",
                          j="AAQ")


def telemetry_params_input(script=SCRIPT):
    return TelemetryParamsInput(page_url="https://example.com/", script=script)


def reese_input(script=SCRIPT):
    return ReeseInput(user_agent="ua", accept_language="en-US", ip="1.2.3.4", pageUrl="https://example.com/",
                      script=script, script_url="https://example.com/r.js", pow="pow")


def slider_input(script=SCRIPT):
    return DataDomeSliderInput(user_agent="ua", device_link="https://geo.captcha-delivery.com/captcha/?initialCid=x",
                               html="<html>", puzzle="pz", piece="pc", parent_url="https://example.com/",
                               accept_language="en-US", ip="1.2.3.4", script=script)


def interstitial_input(script=SCRIPT):
    return DataDomeInterstitialInput(user_agent="ua", device_link="https://geo.captcha-delivery.com/x", html="<html>",
                                     accept_language="en-US", ip="1.2.3.4", script=script)


# Each call: (name, make input, method name, the request body the SDK sent before script hashes)
CALLS = (
    ("sensor", sensor_input, "generate_sensor_data", lambda i: {
        "userAgent": "ua", "abck": "abck", "bmsz": "bmsz", "version": "3", "pageUrl": "https://example.com/",
        "script": SCRIPT, "scriptUrl": "https://example.com/s.js", "context": "", "ip": "1.2.3.4",
        "acceptLanguage": "en-US"}),
    ("telemetry", telemetry_input, "generate_telemetry", lambda i: {
        "userAgent": "ua", "abck": "abck", "bmsz": "bmsz", "version": "", "pageUrl": "https://example.com/",
        "script": SCRIPT, "scriptUrl": "https://example.com/s.js", "context": "", "ip": "1.2.3.4",
        "acceptLanguage": "en-US", "j": "AAQ"}),
    ("telemetry params", telemetry_params_input, "get_telemetry_params", lambda i: {
        "pageUrl": "https://example.com/", "script": SCRIPT, "context": ""}),
    ("sbsd", sbsd_input, "generate_sbsd_data", lambda i: {
        "userAgent": "ua", "uuid": "uuid", "pageUrl": "https://example.com/", "o": "o", "script": SCRIPT,
        "acceptLanguage": "en-US", "ip": "1.2.3.4", "context": ""}),
    ("reese84", reese_input, "generate_reese84_sensor", lambda i: {
        "userAgent": "ua", "acceptLanguage": "en-US", "ip": "1.2.3.4", "scriptUrl": "https://example.com/r.js",
        "pageUrl": "https://example.com/", "pow": "pow", "script": SCRIPT}),
    ("slider", slider_input, "generate_slider_payload", lambda i: i.to_dict()),
    ("interstitial", interstitial_input, "generate_interstitial_payload", lambda i: i.to_dict()),
)


def first_value(res):
    # the payload field is named payload, header (telemetry) or path (telemetry params)
    for field in ("payload", "header", "path"):
        if hasattr(res, field):
            return getattr(res, field)


def hashed(body):
    out = {k: v for k, v in body.items() if k != "script"}
    out["scriptHash"] = SCRIPT_HASH
    return out


class Sync(unittest.TestCase):
    def call(self, api, method, input_data):
        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(api)))
        return getattr(s, method)(input_data)

    def test_unseen_script_sends_the_hash_then_the_script(self):
        for name, make, method, full in CALLS:
            with self.subTest(name):
                api, input_data = FakeAPI(), make()
                before = copy.deepcopy(vars(input_data))
                res = self.call(api, method, input_data)
                self.assertEqual(first_value(res), "p")
                want = full(input_data)
                self.assertEqual(api.sent, [hashed(want), want])
                self.assertEqual(vars(input_data), before)

    def test_known_hash_sends_only_the_hash(self):
        for name, make, method, full in CALLS:
            with self.subTest(name):
                api, input_data = FakeAPI(known={SCRIPT_HASH}), make()
                before = copy.deepcopy(vars(input_data))
                self.call(api, method, input_data)
                self.assertEqual(api.sent, [hashed(full(input_data))])
                self.assertNotIn("script", api.sent[0])
                self.assertEqual(vars(input_data), before)

    def test_script_is_sent_once_then_the_hash_is_reused(self):
        api = FakeAPI()
        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(api)))
        s.generate_sensor_data(sensor_input())
        s.generate_sensor_data(sensor_input())
        self.assertEqual([("script" in b, "scriptHash" in b) for b in api.sent],
                         [(False, True), (True, False), (False, True)])

    def test_error_after_the_script_is_returned(self):
        api = FakeAPI(after_script=(400, {"error": "invalid script"}))
        with self.assertRaisesRegex(Exception, "invalid script"):
            self.call(api, "generate_sensor_data", sensor_input())
        self.assertEqual(len(api.sent), 2)

    def test_second_script_required_is_returned_without_another_retry(self):
        api = FakeAPI(after_script=(422, {"error": "script_required"}))
        with self.assertRaisesRegex(Exception, "script_required"):
            self.call(api, "generate_reese84_sensor", reese_input())
        self.assertEqual(len(api.sent), 2)

    def test_other_answers_to_the_hash_are_returned_as_is(self):
        for status, body, pattern in ((422, {"error": "something else"}, "something else"),
                                      (400, {"error": "bad request"}, "bad request"),
                                      (500, {}, "status code: 500")):
            with self.subTest(status=status, body=body):
                api = lambda request, status=status, body=body: httpx.Response(status, json=body)
                sent = []

                def handler(request, api=api):
                    sent.append(json.loads(request.content))
                    return api(request)

                with self.assertRaisesRegex(Exception, pattern):
                    self.call(handler, "generate_sbsd_data", sbsd_input())
                self.assertEqual(len(sent), 1)
                self.assertIn("scriptHash", sent[0])

    def test_empty_script_requests_are_sent_unchanged(self):
        api = FakeAPI()
        self.call(api, "generate_sensor_data", sensor_input(script="", context="ctx"))
        self.call(api, "generate_sbsd_data", sbsd_input(script="", context="ctx"))
        self.call(api, "generate_reese84_sensor", reese_input(script=""))
        self.call(api, "generate_slider_payload", slider_input(script=""))
        self.assertEqual(len(api.sent), 4)
        for body in api.sent:
            self.assertNotIn("scriptHash", body)
        self.assertEqual((api.sent[0]["script"], api.sent[0]["context"]), ("", "ctx"))
        self.assertEqual((api.sent[1]["script"], api.sent[1]["context"]), ("", "ctx"))
        self.assertEqual(api.sent[2]["script"], "")
        self.assertNotIn("script", api.sent[3])


class Async(unittest.TestCase):
    def call(self, api, method, input_data):
        async def go():
            client = httpx.AsyncClient(transport=httpx.MockTransport(api))
            async with SessionAsync("test-key", client=client) as s:
                res = await getattr(s, method)(input_data)
            await client.aclose()
            return res

        return asyncio.run(go())

    def test_unseen_script_sends_the_hash_then_the_script(self):
        for name, make, method, full in CALLS:
            with self.subTest(name):
                api, input_data = FakeAPI(), make()
                before = copy.deepcopy(vars(input_data))
                res = self.call(api, method, input_data)
                self.assertEqual(first_value(res), "p")
                want = full(input_data)
                self.assertEqual(api.sent, [hashed(want), want])
                self.assertEqual(vars(input_data), before)

    def test_known_hash_sends_only_the_hash(self):
        for name, make, method, full in CALLS:
            with self.subTest(name):
                api = FakeAPI(known={SCRIPT_HASH})
                self.call(api, method, make())
                self.assertEqual(api.sent, [hashed(full(make()))])

    def test_error_after_the_script_is_returned(self):
        api = FakeAPI(after_script=(400, {"error": "invalid script"}))
        with self.assertRaisesRegex(Exception, "invalid script"):
            self.call(api, "generate_slider_payload", slider_input())
        self.assertEqual(len(api.sent), 2)

    def test_empty_script_requests_are_sent_unchanged(self):
        api = FakeAPI()
        self.call(api, "generate_sensor_data", sensor_input(script="", context="ctx"))
        self.call(api, "generate_sbsd_data", sbsd_input(script="", context="ctx"))
        self.assertEqual(len(api.sent), 2)
        for body in api.sent:
            self.assertNotIn("scriptHash", body)
            self.assertEqual((body["script"], body["context"]), ("", "ctx"))


class Hash(unittest.TestCase):
    def test_lowercase_hex_sha256_of_utf8(self):
        from hyper_sdk.shared import script_hash
        self.assertEqual(script_hash("abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        self.assertEqual(script_hash(SCRIPT), SCRIPT_HASH)


if __name__ == "__main__":
    unittest.main()
