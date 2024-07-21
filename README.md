# Hyper Solutions SDK for Python

## Installation

To use the Hyper Solutions SDK in your Python project, you need to install it using the following command:

```
pip install hyper-sdk
```

## Usage

### Creating a Session

To start using the SDK, you need to create a new `Session` instance by providing your API key:

```python
from hyper_sdk import Session

session = Session(api_key="your-api-key")
```

You can also optionally set a JWT key and a custom HTTP client:

```python
from hyper_sdk import Session

session = Session(api_key="your-api-key", jwt_key="your-jwt-key", client=custom_http_client)
```

## Akamai

The Akamai package provides functions for interacting with Akamai Bot Manager, including generating sensor data, parsing script path, parsing pixel challenges, and handling sec-cpt challenges.

### Generating Sensor Data

To generate sensor data required for generating valid Akamai cookies, use the `generate_sensor_data` method:

```python
from hyper_sdk import SensorInput

sensor_input = SensorInput(
    page_url="https://example.com/",
    user_agent="your-user-agent",
    abck="your-abck-cookie",
    bmsz="your-bmsz-cookie",
    version="2.0"
)
sensor_data = session.generate_sensor_data(sensor_input)
```

### Parsing Script Path

To parse the Akamai Bot Manager script path from the given HTML code, use the `parse_script_path` function from the `script_path` module:

```python
from hyper_sdk.akamai.script_path import parse_script_path

script_path = parse_script_path(html_source)
```

### Handling Sec-Cpt Challenges

The Akamai package provides functions for handling sec-cpt challenges:

- `SecCptChallenge.parse`: Parses a sec-cpt challenge from an HTML source.
- `generate_sec_cpt_payload`: Generates a sec-cpt payload using the provided sec-cpt cookie.
- `sleep`: Sleeps for the duration specified in the sec-cpt challenge.

Example usage:

```python
from hyper_sdk.akamai.sec_cpt import SecCptChallenge

challenge = SecCptChallenge.parse(html_source)
payload = challenge.generate_sec_cpt_payload(sec_cpt_cookie)
challenge.sleep()
```

### Validating Cookies

The Akamai package provides functions for validating cookies:

- `is_cookie_valid`: Determines if the provided `_abck` cookie value is valid based on the given request count.
- `is_cookie_invalidated`: Determines if the current session requires more sensors to be sent.

Example usage:

```python
from hyper_sdk.akamai.stop_signal import is_cookie_valid, is_cookie_invalidated

is_valid = is_cookie_valid(abck_cookie, request_count)
is_invalidated = is_cookie_invalidated(abck_cookie)
```

### Generating Pixel Data

To generate pixel data, use the `generate_pixel_data` method:

```python
from hyper_sdk import PixelInput

pixel_input = PixelInput(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    html_var="your-html-var",
    script_var="your-script-var"
)
pixel_data = session.generate_pixel_data(pixel_input)
```

### Parsing Pixel Challenges

The Akamai package provides functions for parsing pixel challenges:

- `parse_pixel_html_var`: Parses the required pixel challenge variable from the given HTML code.
- `parse_pixel_script_url`: Parses the script URL of the pixel challenge script and the URL to post a generated payload to from the given HTML code.
- `parse_pixel_script_var`: Parses the dynamic value from the pixel script.

Example usage:

```python
from hyper_sdk.akamai.pixel import parse_pixel_html_var, parse_pixel_script_url, parse_pixel_script_var

html_var = parse_pixel_html_var(html_source)
script_url, post_url = parse_pixel_script_url(html_source)
script_var = parse_pixel_script_var(script_source)
```


## Incapsula

The Incapsula package provides functions for interacting with Imperva Incapsula, including generating Reese84 sensor data, UTMVC cookies, and parsing UTMVC script paths.

### Generating Reese84 Sensor

To generate sensor data required for generating valid Reese84 cookies, use the `generate_reese84_sensor` method:

```python
sensor_data = session.generate_reese84_sensor(site="example.com", user_agent="your-user-agent")
```

### Generating UTMVC Cookie

To generate the UTMVC cookie using the Hyper Solutions API, use the `generate_utmvc_cookie` method:

```python
from hyper_sdk import UtmvcInput

utmvc_input = UtmvcInput(
    user_agent="your-user-agent",
    session_ids=["session-id-1", "session-id-2"],
    script="your-script"
)
utmvc_cookie = session.generate_utmvc_cookie(utmvc_input)
```

### Parsing UTMVC Script Path

To parse the UTMVC script path from a given script content, use the `parse_utmvc_script_path` function from the `utmvc` module:

```python
from hyper_sdk.incapsula.utmvc import parse_utmvc_script_path

script_path = parse_utmvc_script_path(script_content)
```

### Generating UTMVC Submit Path

To generate a unique UTMVC submit path with a random query parameter, use the `get_utmvc_submit_path` function from the `utmvc` module:

```python
from hyper_sdk.incapsula.utmvc import get_utmvc_submit_path

submit_path = get_utmvc_submit_path()
```

## Kasada

The Kasada package provides functions for interacting with Kasada Bot Manager, including parsing script path.

### Generating Payload Data (CT)

To generate payload data required for generating valid `x-kpsdk-ct` tokens, use the `generate_kasada_payload` function:

```python
payload, headers = hyper_session.generate_kasada_payload(hyper_sdk.KasadaPayloadInput(
    user_agent=USER_AGENT,
    ips_link=ips_link,
    script=ips_script,
    language="en-US"
))
# Use payload and headers for the next request
```

### Generating Pow Data (CD)

To generate POW data (`x-kpsdk-cd`) tokens, use the `generate_kasada_pow` function:

```python
cd = hyper_session.generate_kasada_pow(hyper_sdk.KasadaPowInput(
    st=st,
    work_time=None
))
# Use cd as the x-kpsdk-cd header in the next request
```

### Parsing Script Path

To parse the Kasada script path from the given blocked page (status code 429) HTML code, use the `parse_script_path` function:

```python
from hyper_sdk.kasada import parse_script_path

script_path = parse_script_path(html_content)
# script_path will look like: /ips.js?...
```

## DataDome

The DataDome package provides functions for interacting with DataDome Bot Manager, including parsing device link URLs
for interstitial and slider challenges.

### Generating Interstitial Payload

To generate payload data required for solving interstitial challenges, use the `generate_interstitial_payload` function:

```python
payload = hyper_session.generate_interstitial_payload(hyper_sdk.DataDomeInterstitialInput(
    user_agent=USER_AGENT,
    device_link=device_check_link,
    html=html_content
))
# Use the payload to POST to https://geo.captcha-delivery.com/interstitial/
```

### Generating Slider Payload

To solve DataDome Slider challenges, use the `generate_slider_payload` function:

```python
payload = hyper_session.generate_slider_payload(hyper_sdk.DataDomeSliderInput(
    user_agent=USER_AGENT,
    device_link=device_check_link,
    html=html_content,
    puzzle=base64_encoded_puzzle,
    piece=base64_encoded_piece
))
# Create a GET request to the payload URL
```

### Parsing Interstitial DeviceLink URL

To parse the Interstitial DeviceLink URL from the HTML code, use the `parse_interstitial_device_check_link` function:

```python
from hyper_sdk.datadome import parse_interstitial_device_check_link

device_link = parse_interstitial_device_check_link(html_content, datadome_cookie, referer)
# device_link will look like: https://geo.captcha-delivery.com/interstitial/?...
```

### Parsing Slider DeviceLink URL

To parse the Slider DeviceLink URL from the HTML code, use the `parse_slider_device_check_link` function:

```python
from hyper_sdk.datadome import parse_slider_device_check_link

device_link = parse_slider_device_check_link(html_content, datadome_cookie, referer)
# device_link will look like: https://geo.captcha-delivery.com/captcha/?...
```