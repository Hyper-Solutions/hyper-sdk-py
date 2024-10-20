from typing import Optional, Dict, Any
from urllib.parse import quote

import requests
import jwt
from datetime import datetime, timedelta, timezone

from .akamai_input import SensorInput, PixelInput, DynamicInput, SbsdInput
from .kasada_input import KasadaPowInput, KasadaPayloadInput
from .datadome_input import DataDomeSliderInput, DataDomeInterstitialInput, DataDomeTagsInput
from .incapsula_input import UtmvcInput


class Session:
    def __init__(self, api_key: str, jwt_key: Optional[str] = None, client: Optional[requests.Session] = None) -> None:
        self.api_key = api_key
        self.jwt_key = jwt_key
        self.client = requests.Session() if client is None else client

    def generate_sensor_data(self, input_data: SensorInput) -> str:
        """
            Returns the sensor data required to generate valid akamai cookies using the Hyper Solutions API.

            Args:
                input_data (SensorInput): An instance of SensorInput containing the necessary data for generating the sensor data.

            Returns:
                str: Sensor data as a string.
        """
        sensor_endpoint = "https://akm.justhyped.dev/sensor"
        return self._send_request(sensor_endpoint, {
            'userAgent': input_data.user_agent,
            'abck': input_data.abck,
            'bmsz': input_data.bmsz,
            'version': input_data.version,
            'pageUrl': input_data.page_url,
            'scriptHash': input_data.script_hash,
            'dynamicValues': input_data.dynamic_values,
            'ip': input_data.ip,
            'language': input_data.language,
        })

    def generate_sbsd_data(self, input_data: SbsdInput) -> str:
        """
            Returns the sbsd data required to solve SBSD using the Hyper Solutions API.

            Args:
                input_data (SbsdInput): An instance of SbsdInput containing the necessary data for generating the sbsd data.

            Returns:
                str: Sensor data as a string.
        """
        sensor_endpoint = "https://akm.justhyped.dev/sbsd"
        return self._send_request(sensor_endpoint, {
            'userAgent': input_data.user_agent,
            'uuid': input_data.uuid,
            'pageUrl': input_data.page_url,
            'o': input_data.o_cookie,
            'language': input_data.language,
            'ip': input_data.ip,
        })

    def parse_v3_dynamic(self, input_data: DynamicInput) -> str:
        """
            Returns the dynamic values required to generate sensor data for V3 dynamic with Hyper Solutions API.

            Args:
                input_data (DynamicInput): An instance of DynamicInput containing the necessary data for parsing the script.

            Returns:
                str: Dynamic values as a string.
        """
        sensor_endpoint = "https://akm.justhyped.dev/dynamic"
        return self._send_request(sensor_endpoint, {
            'script': input_data.script,
        })

    def generate_pixel_data(self, input_data: PixelInput) -> str:
        """
            Returns the pixel data using the Hyper Solutions API.

            Args:
                session (Session): An instance of Session to handle the network request.
                input_data (PixelInput): An instance of PixelInput containing the necessary data for generating the pixel data.

            Returns:
                str: Pixel data as a string.
        """
        pixel_endpoint = "https://akm.justhyped.dev/pixel"
        return self._send_request(pixel_endpoint, {
            'userAgent': input_data.user_agent,
            'htmlVar': input_data.html_var,
            'scriptVar': input_data.script_var,
        })

    def generate_reese84_sensor(self, site: str, user_agent: str) -> str:
        """
            Returns the sensor data required to generate valid reese84 cookies using the Hyper Solutions API.

            This function sends a request to the specified sensor endpoint with the necessary data to generate the reese84 sensor data.

            Args:
                site (str): The name of the site that will be used to generate the sensor data.
                user_agent (str): The user agent string used to generate the sensor data.

            Returns:
                str: Sensor data as a string.

            Raises:
                ValueError: If the script attribute in input_data is empty.
        """
        return self._send_request("https://incapsula.justhyped.dev/reese84/" + quote(site),
                                  {
                                      'userAgent': user_agent,
                                  })

    def generate_utmvc_cookie(self, input_data: UtmvcInput) -> str:
        """
            Returns the utmvc cookie using the Hyper Solutions API.

            This function sends a request to the utmvc sensor endpoint with the necessary data to generate the utmvc cookie.
            The input data must include a non-empty script and session IDs.

            Args:
                session (Session): An instance of Session to handle the network request.
                input_data (Input): An instance of Input containing the user agent, session IDs, and script.

            Returns:
                str: The utmvc cookie as a string.

            Raises:
                ValueError: If the script attribute or session IDs in input_data are empty.
        """
        if not input_data.script:
            raise ValueError("script must be non empty")

        if not input_data.session_ids:
            raise ValueError("no session ids set")

        return self._send_request("https://incapsula.justhyped.dev/utmvc", {
            'userAgent': input_data.user_agent,
            'sessionIds': input_data.session_ids,
            'script': input_data.script,
        })

    def generate_kasada_pow(self, input_data: KasadaPowInput) -> str:
        """
            Returns the x-kpsdk-cd value using the Hyper Solutions API.

            Args:
                session (Session): An instance of Session to handle the network request.
                input_data (Input): An instance of Input containing the st and optionally workTime.

            Returns:
                str: The x-kpsdk-cd value as a string.
        """
        return self._send_request("https://kasada.justhyped.dev/cd", input_data.to_dict())

    def generate_kasada_payload(self, input_data: KasadaPayloadInput) -> tuple[str, dict]:
        """
        Returns a base64 encoded payload and headers using the Hyper Solutions API.

        Args: input_data (KasadaPayloadInput): An instance of KasadaPayloadInput containing the userAgent,
        ipsLink and script.

        Returns: tuple[str, dict]: A tuple containing the base64 encoded payload (to POST to /tl) as a string and a
        dictionary of headers.
        """
        if not self.api_key:
            raise ValueError("Missing API key")

        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Api-Key': self.api_key
        }

        if self.jwt_key:
            signature = self.generate_signature()
            headers['X-Signature'] = signature

        response = self.client.post("https://kasada.justhyped.dev/payload", headers=headers, json=input_data.to_dict())

        response_data = response.json()

        if "error" in response_data and response_data["error"]:
            raise Exception(f"API returned with error: {response_data['error']}")

        if response.status_code != 200:
            raise Exception(f"API returned with status code: {response.status_code}")

        return response_data["payload"], response_data["headers"]

    def generate_interstitial_payload(self, input_data: DataDomeInterstitialInput) -> str:
        """
            Returns the DataDome interstitial payload value using the Hyper Solutions API.

            Args:
                session (Session): An instance of Session to handle the network request.
                input_data (DataDomeInterstitialInput): An instance of DataDomeInterstitialInput.

            Returns:
                str: The payload to post to /interstitial/
        """
        return self._send_request("https://datadome.justhyped.dev/interstitial", input_data.to_dict())

    def generate_slider_payload(self, input_data: DataDomeSliderInput) -> str:
        """
            Returns the DataDome Slider URL value using the Hyper Solutions API.

            Args:
                session (Session): An instance of Session to handle the network request.
                input_data (DataDomeSliderInput): An instance of DataDomeSliderInput.

            Returns:
                str: The URL to make a GET request to and returns a solved datadome cookie.
        """
        return self._send_request("https://datadome.justhyped.dev/slider", input_data.to_dict())

    def generate_tags_payload(self, input_data: DataDomeTagsInput) -> str:
        """
            Returns the DataDome Tags payload using the Hyper Solutions API.

            Args:
                session (Session): An instance of Session to handle the network request.
                input_data (DataDomeTagsInput): An instance of DataDomeTagsInput.

            Returns:
                str: The tags payload.
        """
        return self._send_request("https://datadome.justhyped.dev/tags", input_data.to_dict())

    def generate_signature(self) -> str:
        claims = {
            "key": self.api_key,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=60)
        }
        token = jwt.encode(claims, self.jwt_key, algorithm='HS256')
        return token.decode('utf-8')

    def _send_request(self, url: str, input_data: Dict[str, Any]) -> str:
        if not self.api_key:
            raise ValueError("Missing API key")

        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Api-Key': self.api_key
        }

        if self.jwt_key:
            signature = self.generate_signature()
            headers['X-Signature'] = signature

        response = self.client.post(url, headers=headers, json=input_data)

        response_data = response.json()

        if "error" in response_data and response_data["error"]:
            raise Exception(f"API returned with error: {response_data['error']}")

        if response.status_code != 200:
            raise Exception(f"API returned with status code: {response.status_code}")

        return response_data["payload"]
