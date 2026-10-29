"""Runs the real Session / SessionAsync methods against canned API responses."""

import asyncio
import hashlib
import json
import unittest

import httpx

from hyper_sdk import (
    Session, SessionAsync, SensorInput, SbsdInput, TelemetryInput, TelemetryParamsInput, ReeseInput, KasadaPayloadInput,
    KasadaVersionInput,
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
        handler.urls.append(str(request.url))
        return httpx.Response(200, json=body)

    handler.urls = []
    return handler, sent


def sensor_input():
    return SensorInput(abck="", bmsz="", version="3", page_url="", user_agent="", ip="",
                       accept_language="", context="", script="", script_url="")


def telemetry_input(context="", j=""):
    return TelemetryInput(abck="a", bmsz="b", page_url="https://example.com/", user_agent="", ip="",
                          accept_language="", context=context, script="", script_url="", j=j)


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
        telemetry = s.generate_telemetry(telemetry_input())
        self.assertEqual((telemetry.header, telemetry.context, telemetry.client_hints), ("p", "c", HINTS))
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

    def test_telemetry_wire_and_endpoints(self):
        # the flat sensor request plus "j", as /v1/telemetry binds it, and each
        # telemetry method on its own endpoint
        handler, sent = recorder({"payload": "p", "context": "c"})
        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(handler)))
        s.generate_telemetry(telemetry_input(context="ctx", j="AAQ%2f"))
        self.assertEqual(handler.urls[0], "https://akm.hypersolutions.co/v1/telemetry")
        for key, want in (("abck", "a"), ("bmsz", "b"), ("pageUrl", "https://example.com/"), ("context", "ctx"),
                          ("j", "AAQ%2f")):
            self.assertEqual(sent[0][key], want)

        handler, sent = recorder({"payload": "/_bm/get_params?type=web-jsto&v=aN+c/9=", "context": "c"})
        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(handler)))
        res = s.get_telemetry_params(TelemetryParamsInput(page_url="https://example.com/", script="s"))
        self.assertEqual(handler.urls[0], "https://akm.hypersolutions.co/v1/telemetry/params")
        # a script goes out as its hash; this canned API accepts the hash
        self.assertEqual(sent[0], {"pageUrl": "https://example.com/", "context": "",
                                   "scriptHash": hashlib.sha256(b"s").hexdigest()})
        self.assertEqual((res.path, res.context), ("/_bm/get_params?type=web-jsto&v=aN+c/9=", "c"))

    def test_kasada_version(self):
        # the script goes out as-is, never as a hash
        handler, sent = recorder({"payload": "j-1.2.797"})
        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(handler)))
        res = s.get_kasada_version(KasadaVersionInput(page_url="https://example.com/", script="p.js body"))
        self.assertEqual(handler.urls, ["https://kasada.hypersolutions.co/version"])
        self.assertEqual(sent, [{"pageUrl": "https://example.com/", "script": "p.js body"}])
        self.assertEqual(res.version, "j-1.2.797")

        s, _ = self.session({"error": "invalid script"})
        with self.assertRaisesRegex(Exception, "invalid script"):
            s.get_kasada_version(KasadaVersionInput(page_url="https://example.com/", script="p.js body"))

    def test_api_error_still_raises(self):
        s, _ = self.session({"error": "boom"})
        with self.assertRaises(Exception):
            s.generate_sensor_data(sensor_input())


USAGE_PLAN = {"expiresAt": "2027-07-31T00:00:00Z", "requestsUsed": 44235934, "requestsQuota": 9999999999,
              "requestsRemaining": 9955764065, "product": "akamai"}


def usage_handler(status, body):
    """A MockTransport handler for the body-less usage GET that records each request."""
    def handler(request: httpx.Request) -> httpx.Response:
        handler.requests.append(request)
        return httpx.Response(status, json=body)

    handler.requests = []
    return handler


class Usage(unittest.TestCase):
    def check_result(self, res):
        self.assertEqual(res.balance_euro, 12.5)
        self.assertEqual(len(res.plans), 1)
        plan = res.plans[0]
        self.assertEqual((plan.product, plan.requests_used, plan.requests_quota, plan.requests_remaining,
                          plan.expires_at),
                         ("akamai", 44235934, 9999999999, 9955764065, "2027-07-31T00:00:00Z"))

    def check_request(self, handler):
        self.assertEqual(len(handler.requests), 1)
        req = handler.requests[0]
        self.assertEqual((req.method, str(req.url)), ("GET", "https://api.hypersolutions.co/usage"))
        self.assertEqual(req.content, b"")
        self.assertEqual(req.headers["x-api-key"], "test-key")
        self.assertNotIn("content-type", req.headers)

    def test_sync(self):
        handler = usage_handler(200, {"balanceEuro": 12.5, "plans": [USAGE_PLAN]})
        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(handler)))
        self.check_result(s.get_usage())
        self.check_request(handler)

        s = Session("test-key", client=httpx.Client(transport=httpx.MockTransport(
            usage_handler(403, {"error": "Invalid API key"}))))
        with self.assertRaisesRegex(Exception, "Invalid API key"):
            s.get_usage()

    def test_async(self):
        def run(handler):
            async def go():
                client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
                async with SessionAsync("test-key", client=client) as s:
                    res = await s.get_usage()
                await client.aclose()
                return res

            return asyncio.run(go())

        handler = usage_handler(200, {"balanceEuro": 12.5, "plans": [USAGE_PLAN]})
        self.check_result(run(handler))
        self.check_request(handler)
        with self.assertRaisesRegex(Exception, "Invalid API key"):
            run(usage_handler(403, {"error": "Invalid API key"}))


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

    def test_telemetry(self):
        res, sent = self.run_async(BODY, lambda s: s.generate_telemetry(telemetry_input(j="AAQ")))
        self.assertEqual((res.header, res.context, res.client_hints), ("p", "c", HINTS))
        self.assertEqual(sent[0]["j"], "AAQ")
        res, _ = self.run_async({"payload": "/_bm/get_params?type=web-jsto&v=x", "context": "c"},
                                lambda s: s.get_telemetry_params(TelemetryParamsInput(page_url="https://example.com/",
                                                                                     script="s")))
        self.assertEqual((res.path, res.context), ("/_bm/get_params?type=web-jsto&v=x", "c"))

    def test_kasada_version(self):
        version_input = KasadaVersionInput(page_url="https://example.com/", script="p.js body")
        res, sent = self.run_async({"payload": "j-1.2.797"}, lambda s: s.get_kasada_version(version_input))
        self.assertEqual(sent, [{"pageUrl": "https://example.com/", "script": "p.js body"}])
        self.assertEqual(res.version, "j-1.2.797")
        with self.assertRaisesRegex(Exception, "invalid script"):
            self.run_async({"error": "invalid script"}, lambda s: s.get_kasada_version(version_input))

    def test_kasada_payload_and_strict(self):
        res, sent = self.run_async(KASADA_BODY, lambda s: s.generate_kasada_payload(kasada_input(strict=True)))
        self.assertEqual(res.headers["x-kpsdk-ct"], "ct")
        self.assertEqual(res.client_hints["rtt"], "100")
        self.assertIs(sent[0]["strict"], True)


if __name__ == "__main__":
    unittest.main()
