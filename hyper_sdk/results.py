"""Result types returned by the Session and SessionAsync generate_* methods.

Each method returns one of these instead of a tuple or a bare string, so fields
the API adds later become new attributes rather than breaking changes.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# The Accept-CH client hint headers for the device a payload was generated for,
# keyed by lowercase header name, values ready to send verbatim (already
# serialized the way Chrome sends them; do not re-quote). The API returns every
# hint Chrome sends once a site opts in via Accept-CH: the sec-ch-ua-* family,
# sec-ch-device-memory, sec-ch-dpr, sec-ch-viewport-width/height, the legacy
# device-memory, dpr and viewport-width, ect, rtt, downlink and the
# sec-ch-prefers-* preferences. Send only the ones the site asked for in its
# Accept-CH response header. None when the API returned none (Safari user
# agents, and payloads built by a remote browser).
ClientHints = Optional[Dict[str, str]]

__all__ = [
    "ClientHints", "SensorResult", "TelemetryResult", "TelemetryParamsResult", "PixelResult", "SbsdResult",
    "Reese84Result", "UtmvcResult",
    "KasadaPayloadResult", "KasadaVersionResult", "KasadaPowResult", "BotIDHeaderResult", "DataDomeInterstitialResult",
    "DataDomeSliderResult", "DataDomeTagsResult", "TrustDecisionPayloadResult", "TrustDecisionSignatureResult",
    "UsageResult", "UsagePlan",
]


@dataclass
class SensorResult:
    """Returned by generate_sensor_data."""
    payload: str
    """The sensor data to post."""
    context: str
    """Send back as SensorInput.context on the next sensor request."""
    client_hints: ClientHints = None


@dataclass
class TelemetryResult:
    """Returned by generate_telemetry."""
    header: str
    """The ready-to-send value of the Akamai-BM-Telemetry header."""
    context: str
    """Send back as TelemetryInput.context on the next telemetry request."""
    client_hints: ClientHints = None


@dataclass
class TelemetryParamsResult:
    """Returned by get_telemetry_params."""
    path: str
    """The site's get_params path, exactly as the browser requests it. GET it on the
    page's origin; the "j" in its JSON response goes into TelemetryInput.j."""
    context: str
    """Can replace the script on the first generate_telemetry request."""


@dataclass
class PixelResult:
    """Returned by generate_pixel_data."""
    payload: str


@dataclass
class SbsdResult:
    """Returned by generate_sbsd_data."""
    payload: str
    """The sbsd body to post."""
    context: str
    """Send back as SbsdInput.context on the next sbsd request."""
    client_hints: ClientHints = None


@dataclass
class Reese84Result:
    """Returned by generate_reese84_sensor."""
    payload: str
    client_hints: ClientHints = None


@dataclass
class UtmvcResult:
    """Returned by generate_utmvc_cookie."""
    payload: str
    """The ___utmvc cookie value."""
    swhanedl: str


@dataclass
class KasadaPayloadResult:
    """Returned by generate_kasada_payload."""
    payload: str
    """The base64 encoded body to POST to /tl."""
    headers: Dict[str, str]
    """The x-kpsdk-* headers to send with that POST."""
    client_hints: ClientHints = None
    """Accept-CH headers; unlike headers, send only the ones the site asked for."""


@dataclass
class KasadaVersionResult:
    """Returned by get_kasada_version."""
    version: str
    """The x-kpsdk-v value, such as "j-1.2.797". Send it verbatim on the /fp request
    and in the x-kpsdk-v header."""


@dataclass
class UsagePlan:
    """The quota of one plan in a UsageResult."""
    product: str
    """The product the plan covers, such as "akamai" or "datadome"."""
    requests_used: int
    """The number of requests used from the plan."""
    requests_quota: int
    """The number of requests the plan allows."""
    requests_remaining: int
    """requests_quota minus requests_used."""
    expires_at: str
    """When the plan expires, as an ISO 8601 date-time string."""


@dataclass
class UsageResult:
    """Returned by get_usage."""
    balance_euro: float
    """The pay-as-you-go balance in euros."""
    plans: List[UsagePlan]
    """The plans of the API key, one per product."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UsageResult":
        return cls(
            balance_euro=data["balanceEuro"],
            plans=[
                UsagePlan(
                    product=plan["product"],
                    requests_used=plan["requestsUsed"],
                    requests_quota=plan["requestsQuota"],
                    requests_remaining=plan["requestsRemaining"],
                    expires_at=plan["expiresAt"],
                )
                for plan in data["plans"]
            ],
        )


@dataclass
class KasadaPowResult:
    """Returned by generate_kasada_pow."""
    payload: str
    """The x-kpsdk-cd value."""


@dataclass
class BotIDHeaderResult:
    """Returned by generate_botid_header."""
    payload: str
    """The x-is-human header value."""


@dataclass
class DataDomeInterstitialResult:
    """Returned by generate_interstitial_payload."""
    payload: str
    """The body to POST to /interstitial/."""
    client_hints: ClientHints = None


@dataclass
class DataDomeSliderResult:
    """Returned by generate_slider_payload."""
    payload: str
    """The URL to GET for a solved datadome cookie."""
    client_hints: ClientHints = None


@dataclass
class DataDomeTagsResult:
    """Returned by generate_tags_payload."""
    payload: str
    client_hints: ClientHints = None


@dataclass
class TrustDecisionPayloadResult:
    """Returned by generate_trustdecision_payload."""
    payload: str
    """The payload to post to TrustDecision's fingerprinting endpoint."""
    time_zone: str
    """The value for the tz header on subsequent requests."""
    client_id: str
    """Needed to generate session signatures."""


@dataclass
class TrustDecisionSignatureResult:
    """Returned by generate_trustdecision_signature."""
    payload: str
    """The single-use td-session-sign header value."""
