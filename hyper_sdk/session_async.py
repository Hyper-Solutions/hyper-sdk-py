"""Async version of the Session class for Hyper Solutions API."""

from typing import Optional, Dict, Any, Tuple
import httpx
import json
import gzip

from .shared import generate_signature, build_headers, validate_response
from .akamai_input import SensorInput, PixelInput, SbsdInput
from .kasada_input import KasadaPowInput, KasadaPayloadInput, BotIDHeaderInput
from .datadome_input import DataDomeSliderInput, DataDomeInterstitialInput, DataDomeTagsInput
from .incapsula_input import UtmvcInput, ReeseInput
from .trustdecision_input import PayloadInput, DecodeInput, SignatureInput
from .results import (
    SensorResult, PixelResult, SbsdResult, Reese84Result, UtmvcResult, KasadaPayloadResult,
    KasadaPowResult, BotIDHeaderResult, DataDomeInterstitialResult, DataDomeSliderResult,
    DataDomeTagsResult, TrustDecisionPayloadResult, TrustDecisionSignatureResult,
)
from .payloads import sensor_payload, sbsd_payload, pixel_payload, reese84_payload, utmvc_payload, \
    trustdecision_payload


class SessionAsync:
    def __init__(self, api_key: str, jwt_key: Optional[str] = None, app_key: Optional[str] = None,
                 app_secret: Optional[str] = None, client: Optional[httpx.AsyncClient] = None,
                 compression: bool = True) -> None:
        self.api_key = api_key
        self.jwt_key = jwt_key
        self.app_key = app_key
        self.app_secret = app_secret
        self.client = client
        self._owns_client = client is None
        self.compression = compression

    async def __aenter__(self):
        if self._owns_client:
            self.client = httpx.AsyncClient(http2=True, timeout=httpx.Timeout(30.0))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._owns_client and self.client:
            await self.client.aclose()

    async def ensure_client(self):
        """Ensure we have an active client session."""
        if self.client is None:
            self.client = httpx.AsyncClient(http2=True, timeout=httpx.Timeout(30.0))
            self._owns_client = True

    async def close(self):
        """Close the client session if we own it."""
        if self._owns_client and self.client:
            await self.client.aclose()

    async def generate_sensor_data(self, input_data: SensorInput) -> SensorResult:
        """
        Returns the sensor data required to generate valid akamai cookies using the Hyper Solutions API.

        Args:
            input_data (SensorInput): An instance of SensorInput containing the necessary data for generating the sensor data.

        Returns:
            SensorResult: payload (sensor data), context (for the next sensor request) and client_hints.
        """
        data = await self._post("https://akm.hypersolutions.co/v2/sensor", sensor_payload(input_data))
        return SensorResult(data["payload"], data.get("context", ""), data.get("headers"))

    async def generate_sbsd_data(self, input_data: SbsdInput) -> SbsdResult:
        """
        Returns the sbsd data required to solve SBSD using the Hyper Solutions API.

        Args:
            input_data (SbsdInput): An instance of SbsdInput containing the necessary data for generating the sbsd data.

        Returns:
            SbsdResult: payload (sbsd data), context (for the next sbsd request) and client_hints.
        """
        data = await self._post("https://akm.hypersolutions.co/sbsd", sbsd_payload(input_data))
        return SbsdResult(data["payload"], data.get("context", ""), data.get("headers"))

    async def generate_pixel_data(self, input_data: PixelInput) -> PixelResult:
        """
        Returns the pixel data using the Hyper Solutions API.

        Args:
            input_data (PixelInput): An instance of PixelInput containing the necessary data for generating the pixel data.

        Returns:
            PixelResult: payload (pixel data).
        """
        data = await self._post("https://akm.hypersolutions.co/pixel", pixel_payload(input_data))
        return PixelResult(data["payload"])

    async def generate_reese84_sensor(self, input_data: ReeseInput) -> Reese84Result:
        """
        Returns the sensor data required to generate valid reese84 cookies using the Hyper Solutions API.

        Args:
            input_data (ReeseInput): The input data.

        Returns:
            Reese84Result: payload (sensor data) and client_hints (None for Safari user agents).
        """
        data = await self._post("https://incapsula.hypersolutions.co/reese84", reese84_payload(input_data))
        return Reese84Result(data["payload"], data.get("headers"))

    async def generate_utmvc_cookie(self, input_data: UtmvcInput) -> UtmvcResult:
        """
        Returns the utmvc cookie using the Hyper Solutions API.

        The input data must include a non-empty script and session IDs.

        Args:
            input_data (UtmvcInput): An instance of UtmvcInput containing the user agent, session IDs, and script.

        Returns:
            UtmvcResult: payload (the utmvc cookie) and swhanedl.
        """
        data = await self._post("https://incapsula.hypersolutions.co/utmvc", utmvc_payload(input_data))
        return UtmvcResult(data["payload"], data["swhanedl"])

    async def generate_kasada_pow(self, input_data: KasadaPowInput) -> KasadaPowResult:
        """
        Returns the x-kpsdk-cd value using the Hyper Solutions API.

        Args:
            input_data (KasadaPowInput): An instance of KasadaPowInput containing the st and optionally workTime.

        Returns:
            KasadaPowResult: payload (the x-kpsdk-cd value).
        """
        data = await self._post("https://kasada.hypersolutions.co/cd", input_data.to_dict())
        return KasadaPowResult(data["payload"])

    async def generate_kasada_payload(self, input_data: KasadaPayloadInput) -> KasadaPayloadResult:
        """
        Returns a base64 encoded payload, its x-kpsdk-* headers and the client hints using the Hyper Solutions API.

        Args:
            input_data (KasadaPayloadInput): An instance of KasadaPayloadInput containing the userAgent,
            ipsLink and script.

        Returns:
            KasadaPayloadResult: payload (base64, to POST to /tl), headers (x-kpsdk-*) and client_hints.
        """
        data = await self._post("https://kasada.hypersolutions.co/payload", input_data.to_dict())
        return KasadaPayloadResult(data["payload"], data["headers"], data.get("clientHints"))

    async def generate_botid_header(self, input_data: BotIDHeaderInput) -> BotIDHeaderResult:
        """
        Returns the x-is-human header value for Vercel BotID using the Hyper Solutions API.

        Args:
            input_data (BotIDHeaderInput): An instance of BotIDHeaderInput containing the script,
                user agent, IP, and accept language.

        Returns:
            BotIDHeaderResult: payload (the x-is-human header value).
        """
        data = await self._post("https://kasada.hypersolutions.co/botid", input_data.to_dict())
        return BotIDHeaderResult(data["payload"])

    async def generate_interstitial_payload(self, input_data: DataDomeInterstitialInput) -> DataDomeInterstitialResult:
        """
        Returns the DataDome interstitial payload using the Hyper Solutions API.

        Args:
            input_data (DataDomeInterstitialInput): An instance of DataDomeInterstitialInput.

        Returns:
            DataDomeInterstitialResult: payload (to post to /interstitial/) and client_hints.
        """
        data = await self._post("https://datadome.hypersolutions.co/interstitial", input_data.to_dict())
        return DataDomeInterstitialResult(data["payload"], data.get("headers"))

    async def generate_slider_payload(self, input_data: DataDomeSliderInput) -> DataDomeSliderResult:
        """
        Returns the DataDome Slider URL using the Hyper Solutions API.

        Args:
            input_data (DataDomeSliderInput): An instance of DataDomeSliderInput.

        Returns:
            DataDomeSliderResult: payload (the URL to GET for a solved datadome cookie) and client_hints.
        """
        data = await self._post("https://datadome.hypersolutions.co/slider", input_data.to_dict())
        return DataDomeSliderResult(data["payload"], data.get("headers"))

    async def generate_tags_payload(self, input_data: DataDomeTagsInput) -> DataDomeTagsResult:
        """
        Returns the DataDome Tags payload using the Hyper Solutions API.

        Args:
            input_data (DataDomeTagsInput): An instance of DataDomeTagsInput.

        Returns:
            DataDomeTagsResult: payload (the tags payload) and client_hints.
        """
        data = await self._post("https://datadome.hypersolutions.co/tags", input_data.to_dict())
        return DataDomeTagsResult(data["payload"], data.get("headers"))

    async def generate_trustdecision_payload(self, input_data: PayloadInput) -> TrustDecisionPayloadResult:
        """
        Generates TrustDecision payload that should be posted to TrustDecision's fingerprinting endpoint.
        Also returns timezone and clientId required for subsequent operations.

        Args:
            input_data (PayloadInput): An instance of PayloadInput containing the necessary data for generating the payload.

        Returns:
            TrustDecisionPayloadResult: payload (for the fingerprinting endpoint), time_zone (for the tz header on
            subsequent requests) and client_id (for generating session signatures).
        """
        data = await self._post("https://trustdecision.hypersolutions.co/payload", trustdecision_payload(input_data))
        return TrustDecisionPayloadResult(data["payload"], data["timeZone"], data["clientId"])

    async def decode_trustdecision_session_key(self, input_data: DecodeInput) -> str:
        """
        Decodes the result and requestId from TrustDecision's fingerprinting endpoint
        to generate the td-session-key header value.

        Args:
            input_data (DecodeInput): An instance of DecodeInput containing the result and requestId.

        Returns:
            str: The decoded session key value for use in the td-session-key header
        """
        data = await self._post("https://trustdecision.hypersolutions.co/decode", {
            'result': input_data.result,
            'requestId': input_data.request_id,
        })
        return data["payload"]

    async def generate_trustdecision_signature(self, input_data: SignatureInput) -> TrustDecisionSignatureResult:
        """
        Generates a unique td-session-sign header value for each API request.
        This signature can only be used once and must be regenerated for every request.

        Args:
            input_data (SignatureInput): An instance of SignatureInput containing the clientId and path.

        Returns:
            TrustDecisionSignatureResult: payload (the single-use td-session-sign header value).
        """
        data = await self._post("https://trustdecision.hypersolutions.co/sign", {
            'clientId': input_data.client_id,
            'path': input_data.path,
        })
        return TrustDecisionSignatureResult(data["payload"])

    def generate_signature(self, key: str, secret: str) -> str:
        """
        Generates a JWT signature using the provided key and secret.

        Args:
            key (str): The key to include in the JWT claims
            secret (str): The secret used to sign the JWT

        Returns:
            str: The generated JWT token
        """
        return generate_signature(key, secret)

    def _build_headers(self) -> Dict[str, str]:
        """
        Builds the headers dictionary including organization credentials if available.

        Returns:
            Dict[str, str]: Headers dictionary with all required authentication headers
        """
        headers = build_headers(self.api_key, self.jwt_key, self.app_key, self.app_secret)
        # Add compression headers
        if self.compression:
            headers["accept-encoding"] = "gzip"
        return headers

    def _compress_payload(self, payload: bytes) -> Tuple[bytes, bool]:
        """
        Compresses the payload using gzip if enabled and payload is large enough.

        Args:
            payload (bytes): The payload to potentially compress

        Returns:
            Tuple[bytes, bool]: The (potentially compressed) payload and whether compression was used
        """
        if not self.compression or len(payload) <= 1000:
            return payload, False

        try:
            compressed = gzip.compress(payload, compresslevel=6)
            return compressed, True
        except Exception:
            # Fall back to uncompressed if compression fails
            return payload, False

    def _decompress_response(self, response: httpx.Response) -> bytes:
        """
        Decompresses the response body if it's compressed with gzip.

        Args:
            response (httpx.Response): The HTTP response

        Returns:
            bytes: The decompressed response body
        """
        content = response.content
        content_encoding = response.headers.get("content-encoding", "").lower()

        if content_encoding == "gzip" and self.compression:
            try:
                return gzip.decompress(content)
            except Exception:
                # Fall back to original content if decompression fails
                pass

        return content

    async def _post(self, url: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request and returns the validated response body.

        Args:
            url (str): The endpoint URL
            input_data (Dict[str, Any]): The request data

        Returns:
            Dict[str, Any]: The decoded response body
        """
        await self.ensure_client()
        headers = self._build_headers()
        payload = json.dumps(input_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "gzip"

        response = await self.client.post(url, headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)
        return response_data
