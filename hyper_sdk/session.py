"""Session class for Hyper Solutions API."""

from typing import Optional, Dict, Any, Tuple
from urllib.parse import quote
import httpx
import json
import zstandard as zstd

from .shared import generate_signature, build_headers, validate_response
from .akamai_input import SensorInput, PixelInput, SbsdInput
from .kasada_input import KasadaPowInput, KasadaPayloadInput
from .datadome_input import DataDomeSliderInput, DataDomeInterstitialInput, DataDomeTagsInput
from .incapsula_input import UtmvcInput, ReeseInput
from .trustdecision_input import PayloadInput, DecodeInput, SignatureInput


class Session:
    def __init__(self, api_key: str, jwt_key: Optional[str] = None, app_key: Optional[str] = None,
                 app_secret: Optional[str] = None, client: Optional[httpx.Client] = None,
                 compression: bool = True) -> None:
        self.api_key = api_key
        self.jwt_key = jwt_key
        self.app_key = app_key
        self.app_secret = app_secret
        self.client = httpx.Client() if client is None else client
        self._owns_client = client is None
        self.compression = compression and zstd is not None

        # Initialize zstd compressor and decompressor if available
        if self.compression:
            self._compressor = zstd.ZstdCompressor(level=3)
            self._decompressor = zstd.ZstdDecompressor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._owns_client and self.client:
            self.client.close()

    def close(self):
        """Close the client if we own it."""
        if self._owns_client and self.client:
            self.client.close()

    def generate_sensor_data(self, input_data: SensorInput) -> Tuple[str, str]:
        """
        Returns the sensor data required to generate valid akamai cookies using the Hyper Solutions API.

        Args:
            input_data (SensorInput): An instance of SensorInput containing the necessary data for generating the sensor data.

        Returns:
            str: Sensor data as a string.
            str: Context data as a string.
        """
        sensor_endpoint = "https://akm.hypersolutions.co/v2/sensor"

        headers = self._build_headers()
        payload_data = {
            'userAgent': input_data.user_agent,
            'abck': input_data.abck,
            'bmsz': input_data.bmsz,
            'version': input_data.version,
            'pageUrl': input_data.page_url,
            'script': input_data.script,
            'context': input_data.context,
            'ip': input_data.ip,
            'acceptLanguage': input_data.acceptLanguage,
            'scriptUrl': input_data.scriptUrl,
        }
        payload = json.dumps(payload_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "zstd"

        response = self.client.post(sensor_endpoint, headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)

        return response_data["payload"], response_data.get("context", "")

    def generate_sbsd_data(self, input_data: SbsdInput) -> str:
        """
        Returns the sbsd data required to solve SBSD using the Hyper Solutions API.

        Args:
            input_data (SbsdInput): An instance of SbsdInput containing the necessary data for generating the sbsd data.

        Returns:
            str: Sensor data as a string.
        """
        sensor_endpoint = "https://akm.hypersolutions.co/sbsd"
        return self._send_request(sensor_endpoint, {
            'userAgent': input_data.user_agent,
            'uuid': input_data.uuid,
            'pageUrl': input_data.page_url,
            'o': input_data.o_cookie,
            'script': input_data.script,
            'acceptLanguage': input_data.acceptLanguage,
            'ip': input_data.ip,
            'index': input_data.index,
        })

    def generate_pixel_data(self, input_data: PixelInput) -> str:
        """
        Returns the pixel data using the Hyper Solutions API.

        Args:
            input_data (PixelInput): An instance of PixelInput containing the necessary data for generating the pixel data.

        Returns:
            str: Pixel data as a string.
        """
        pixel_endpoint = "https://akm.hypersolutions.co/pixel"
        return self._send_request(pixel_endpoint, {
            'userAgent': input_data.user_agent,
            'htmlVar': input_data.html_var,
            'scriptVar': input_data.script_var,
            'ip': input_data.ip,
            'acceptLanguage': input_data.acceptLanguage,
        })

    def generate_reese84_sensor(self, site: str, input_data: ReeseInput) -> str:
        """
        Returns the sensor data required to generate valid reese84 cookies using the Hyper Solutions API.

        This function sends a request to the specified sensor endpoint with the necessary data to generate the reese84 sensor data.

        Args:
            site (str): The name of the site that will be used to generate the sensor data.
            input_data (ReeseInput): The input data.

        Returns:
            str: Sensor data as a string.

        Raises:
            ValueError: If the script attribute in input_data is empty.
        """
        return self._send_request("https://incapsula.hypersolutions.co/reese84/" + quote(site), {
            'userAgent': input_data.user_agent,
            'acceptLanguage': input_data.acceptLanguage,
            'ip': input_data.ip,
            'scriptUrl': input_data.scriptUrl,
            'pageUrl': input_data.pageUrl,
            'pow': input_data.pow,
            'script': input_data.script,
        })

    def generate_utmvc_cookie(self, input_data: UtmvcInput) -> Tuple[str, str]:
        """
        Returns the utmvc cookie using the Hyper Solutions API.

        This function sends a request to the utmvc sensor endpoint with the necessary data to generate the utmvc cookie.
        The input data must include a non-empty script and session IDs.

        Args:
            input_data (UtmvcInput): An instance of UtmvcInput containing the user agent, session IDs, and script.

        Returns:
            str: The utmvc cookie as a string.
            str: The swhanedl parameter.

        Raises:
            ValueError: If the script attribute or session IDs in input_data are empty.
        """
        headers = self._build_headers()
        payload_data = {
            'userAgent': input_data.user_agent,
            'sessionIds': input_data.session_ids,
            'script': input_data.script,
        }
        payload = json.dumps(payload_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "zstd"

        response = self.client.post("https://incapsula.hypersolutions.co/utmvc", headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)

        return response_data["payload"], response_data["swhanedl"]

    def generate_kasada_pow(self, input_data: KasadaPowInput) -> str:
        """
        Returns the x-kpsdk-cd value using the Hyper Solutions API.

        Args:
            input_data (KasadaPowInput): An instance of KasadaPowInput containing the st and optionally workTime.

        Returns:
            str: The x-kpsdk-cd value as a string.
        """
        return self._send_request("https://kasada.hypersolutions.co/cd", input_data.to_dict())

    def generate_kasada_payload(self, input_data: KasadaPayloadInput) -> Tuple[str, dict]:
        """
        Returns a base64 encoded payload and headers using the Hyper Solutions API.

        Args:
            input_data (KasadaPayloadInput): An instance of KasadaPayloadInput containing the userAgent,
            ipsLink and script.

        Returns:
            tuple[str, dict]: A tuple containing the base64 encoded payload (to POST to /tl) as a string and a
            dictionary of headers.
        """
        headers = self._build_headers()
        payload_data = input_data.to_dict()
        payload = json.dumps(payload_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "zstd"

        response = self.client.post("https://kasada.hypersolutions.co/payload", headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)

        return response_data["payload"], response_data["headers"]

    def generate_interstitial_payload(self, input_data: DataDomeInterstitialInput) -> Dict[str, Any]:
        """
        Returns the DataDome interstitial payload value and response headers using the Hyper Solutions API.

        Args:
            input_data (DataDomeInterstitialInput): An instance of DataDomeInterstitialInput.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - payload (str): The payload to post to /interstitial/
                - headers (Dict[str, str]): The response headers
        """
        return self._send_request_with_headers("https://datadome.hypersolutions.co/interstitial", input_data.to_dict())

    def generate_slider_payload(self, input_data: DataDomeSliderInput) -> Dict[str, Any]:
        """
        Returns the DataDome Slider URL value and response headers using the Hyper Solutions API.

        Args:
            input_data (DataDomeSliderInput): An instance of DataDomeSliderInput.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - payload (str): The URL to make a GET request to for a solved datadome cookie
                - headers (Dict[str, str]): The response headers
        """
        return self._send_request_with_headers("https://datadome.hypersolutions.co/slider", input_data.to_dict())

    def generate_tags_payload(self, input_data: DataDomeTagsInput) -> str:
        """
        Returns the DataDome Tags payload using the Hyper Solutions API.

        Args:
            input_data (DataDomeTagsInput): An instance of DataDomeTagsInput.

        Returns:
            str: The tags payload.
        """
        return self._send_request("https://datadome.hypersolutions.co/tags", input_data.to_dict())

    def generate_trustdecision_payload(self, input_data: PayloadInput) -> Tuple[str, str, str]:
        """
        Generates TrustDecision payload that should be posted to TrustDecision's fingerprinting endpoint.
        Also returns timezone and clientId required for subsequent operations.

        Args:
            input_data (PayloadInput): An instance of PayloadInput containing the necessary data for generating the payload.

        Returns:
            Tuple[str, str, str]: A tuple containing:
                - payload (str): The generated TrustDecision payload for posting to the fingerprinting endpoint
                - timeZone (str): The timezone to use in the tz header for subsequent requests
                - clientId (str): The client ID required for generating session signatures
        """
        headers = self._build_headers()
        payload_data = {
            'userAgent': input_data.user_agent,
            'pageUrl': input_data.page_url,
            'fpUrl': input_data.fp_url,
            'ip': input_data.ip,
            'acceptLanguage': input_data.accept_language,
            'script': input_data.script,
        }
        payload = json.dumps(payload_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "zstd"

        response = self.client.post("https://trustdecision.hypersolutions.co/payload", headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)

        return response_data["payload"], response_data["timeZone"], response_data["clientId"]

    def decode_trustdecision_session_key(self, input_data: DecodeInput) -> str:
        """
        Decodes the result and requestId from TrustDecision's fingerprinting endpoint
        to generate the td-session-key header value.

        Args:
            input_data (DecodeInput): An instance of DecodeInput containing the result and requestId.

        Returns:
            str: The decoded session key value for use in the td-session-key header
        """
        return self._send_request("https://trustdecision.hypersolutions.co/decode", {
            'result': input_data.result,
            'requestId': input_data.request_id,
        })

    def generate_trustdecision_signature(self, input_data: SignatureInput) -> str:
        """
        Generates a unique td-session-sign header value for each API request.
        This signature can only be used once and must be regenerated for every request.

        Args:
            input_data (SignatureInput): An instance of SignatureInput containing the clientId and path.

        Returns:
            str: The generated signature value for use in the td-session-sign header (single-use only)
        """
        return self._send_request("https://trustdecision.hypersolutions.co/sign", {
            'clientId': input_data.client_id,
            'path': input_data.path,
        })

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
            headers["accept-encoding"] = "zstd"
        return headers

    def _compress_payload(self, payload: bytes) -> Tuple[bytes, bool]:
        """
        Compresses the payload using zstd if enabled and payload is large enough.

        Args:
            payload (bytes): The payload to potentially compress

        Returns:
            Tuple[bytes, bool]: The (potentially compressed) payload and whether compression was used
        """
        if not self.compression or len(payload) <= 1000:
            return payload, False

        try:
            compressed = self._compressor.compress(payload)
            return compressed, True
        except Exception:
            # Fall back to uncompressed if compression fails
            return payload, False

    def _decompress_response(self, response: httpx.Response) -> bytes:
        """
        Decompresses the response body if it's compressed with zstd.

        Args:
            response (httpx.Response): The HTTP response

        Returns:
            bytes: The decompressed response body
        """
        content = response.content
        content_encoding = response.headers.get("content-encoding", "").lower()

        if content_encoding == "zstd" and self.compression:
            try:
                return self._decompressor.decompress(content)
            except Exception:
                # Fall back to original content if decompression fails
                pass

        return content

    def _send_request(self, url: str, input_data: Dict[str, Any]) -> str:
        """
        Sends a request and returns the payload.

        Args:
            url (str): The endpoint URL
            input_data (Dict[str, Any]): The request data

        Returns:
            str: The response payload
        """
        headers = self._build_headers()
        payload = json.dumps(input_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "zstd"

        response = self.client.post(url, headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)
        return response_data["payload"]

    def _send_request_with_headers(self, url: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request and returns the payload with headers.

        Args:
            url (str): The endpoint URL
            input_data (Dict[str, Any]): The request data

        Returns:
            Dict[str, Any]: Dictionary containing payload and headers
        """
        headers = self._build_headers()
        payload = json.dumps(input_data).encode('utf-8')

        # Compress payload if large enough
        payload, use_compression = self._compress_payload(payload)
        if use_compression:
            headers["content-encoding"] = "zstd"

        response = self.client.post(url, headers=headers, content=payload)

        # Decompress response if needed
        response_content = self._decompress_response(response)
        response_data = json.loads(response_content)
        validate_response(response_data, response.status_code)
        return {
            "payload": response_data["payload"],
            "headers": response_data["headers"]
        }