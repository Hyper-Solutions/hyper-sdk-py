# Hyper Solutions SDK - Python Library for Bot Protection Bypass (Akamai, Incapsula, Kasada, DataDome)

![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI Version](https://img.shields.io/pypi/v/hyper-sdk)
![PyPI Downloads](https://img.shields.io/pypi/dm/hyper-sdk)

[![](https://dcbadge.limes.pink/api/server/akamai)](https://discord.gg/akamai)

A powerful **Python SDK** for bypassing modern bot protection systems including **Akamai Bot Manager**, **Incapsula**, **Kasada**, and **DataDome**. Generate valid cookies, solve anti-bot challenges, and automate protected endpoints with ease.

Perfect for **web scraping**, **automation**, and **data collection** from protected websites.

## 🔑 Getting API Access

Before using this SDK, you'll need an API key from Hyper Solutions:

1. **Visit [hypersolutions.co](https://hypersolutions.co/?utm_source=github&utm_medium=sdk_readme&utm_campaign=python_sdk_api_access)** to create your account
2. **Choose your plan**:
    - 💳 **Pay-as-you-go**: Perfect for testing and small-scale usage
    - 📊 **Subscription plans**: Cost-effective for high-volume applications
3. **Get your API key** from the dashboard
4. **Start bypassing bot protection** with this SDK!

## 🚀 Quick Start

```python
from hyper_sdk import Session, SensorInput

session = Session("your-api-key")

# Generate Akamai sensor data
sensor_data, sensor_context = session.generate_sensor_data(SensorInput(
    # sensor input fields
))

print(f"Generated sensor data: {sensor_data}")
print(f"Sensor context: {sensor_context}")
```

## ✨ Features

- 🛡️ **Akamai Bot Manager**: Generate sensor data, handle pixel challenges, validate cookies
- 🔒 **Incapsula Protection**: Generate Reese84 sensors and UTMVC cookies
- ⚡ **Kasada Bypass**: Generate payload data (CT) and POW tokens (CD)
- 🎯 **DataDome Solutions**: Solve tags, slider captchas and interstitial challenges
- 🔧 **Easy Integration**: Simple Python API with async/await support
- ⚙️ **Flexible Configuration**: Custom HTTP clients and session management

## 📦 Installation

Install the Hyper Solutions SDK for Python using:

```bash
pip install hyper-sdk
```

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Basic Usage](#-basic-usage)
- [Akamai Bot Manager](#-akamai-bot-manager)
- [Incapsula Protection](#-incapsula-protection)
- [Kasada Bypass](#-kasada-bypass)
- [DataDome Solutions](#-datadome-solutions)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🔧 Basic Usage

### Creating a Session

Initialize the SDK with your API key to start bypassing bot protection:

```python
from hyper_sdk import Session

# Basic session
session = Session("your-api-key")

# Advanced session with custom configuration
session = Session(
    api_key="your-api-key",
    jwt_key="your-jwt-key",
    app_key="your-app-key",
    app_secret="your-app-secret",
    client=custom_http_client
)
```

## 🛡️ Akamai Bot Manager

Bypass **Akamai Bot Manager** protection with sensor data generation, cookie validation, and challenge solving.

### Generating Sensor Data

Generate sensor data for valid **Akamai cookies** and bot detection bypass:

```python
sensor_data, context = await session.generate_sensor_data({
    # Configure sensor parameters
})
```

### Handling Sec-Cpt Challenges

Solve **sec-cpt challenges** with built-in parsing and payload generation:

```python
from hyper_sdk.akamai import SecCptChallenge

# Parse sec-cpt challenge from HTML
challenge = SecCptChallenge.parse(html_content)

# Or parse from JSON response
challenge = SecCptChallenge.parse_from_json(json_response)

# Generate challenge response payload
payload = challenge.generate_sec_cpt_payload(sec_cpt_cookie)

# Handle challenge timing requirements
challenge.sleep()
```

### Cookie Validation

Validate **Akamai _abck cookies** and session states:

```python
from hyper_sdk.akamai import is_cookie_valid, is_cookie_invalidated

# Check if cookie is valid for the current request count
is_valid = is_cookie_valid(cookie_value, request_count)

# Check if cookie has been invalidated and needs refresh
needs_refresh = is_cookie_invalidated(cookie_value)
```

### Pixel Challenge Solving

Handle **Akamai pixel challenges** for advanced bot detection bypass:

```python
from hyper_sdk import PixelInput
from hyper_sdk.akamai import parse_pixel_html_var, parse_pixel_script_url, parse_pixel_script_var

# Parse pixel challenge data
html_var = parse_pixel_html_var(html_content)
script_url, post_url = parse_pixel_script_url(html_content)
script_var = parse_pixel_script_var(script_content)

# Generate pixel data
pixel_data = session.generate_pixel_data(PixelInput(
    # pixel input fields
))
```

## 🔒 Incapsula Protection

Bypass **Incapsula bot detection** with Reese84 sensors and UTMVC cookie generation.

### Generating Reese84 Sensors

Create **Reese84 sensor data** for Incapsula bypass:

```python
from hyper_sdk import ReeseInput

sensor_data = session.generate_reese84_sensor("example.com", ReeseInput(
    # reese input fields
))
```

### UTMVC Cookie Generation

Generate **UTMVC cookies** for Incapsula protection bypass:

```python
from hyper_sdk import UtmvcInput

utmvc_cookie, swhanedl = session.generate_utmvc_cookie(UtmvcInput(
    # utmvc input fields
))
```

### Script Path Parsing

Parse **UTMVC script paths** and generate submit paths:

```python
from hyper_sdk.incapsula import parse_utmvc_script_path, get_utmvc_submit_path

# Parse script path from content
script_path = parse_utmvc_script_path(script_content)

# Generate unique submit path
submit_path = get_utmvc_submit_path()
```

### Dynamic Reese Script Parsing

Parse dynamic Reese84 script paths from interruption pages:

```python
from hyper_sdk.incapsula import parse_dynamic_reese_script

sensor_path, script_path = parse_dynamic_reese_script(html_content, "https://example.com")
```

## ⚡ Kasada Bypass

Defeat **Kasada Bot Manager** with payload generation and POW solving.

### Generating Payload Data (CT)

Create **x-kpsdk-ct tokens** for Kasada bypass:

```python
from hyper_sdk import KasadaPayloadInput

payload, headers = session.generate_kasada_payload(KasadaPayloadInput(
    # kasada payload input fields
))
```

### Generating POW Data (CD)

Solve **Kasada Proof-of-Work** challenges for x-kpsdk-cd tokens:

```python
from hyper_sdk import KasadaPowInput

pow_payload = session.generate_kasada_pow(KasadaPowInput(
    # kasada pow input fields
))
```

## 🤖 Vercel BotID

Bypass **Vercel BotID** protection by generating the required `x-is-human` header.

### Generating the x-is-human Header

Create the **x-is-human header** for Vercel BotID bypass:

```python
from hyper_sdk import BotIDHeaderInput

header = session.generate_botid_header(BotIDHeaderInput(
    script=script_body,          # The c.js script content
    user_agent="your-user-agent",
    ip="your-proxy-ip",
    accept_language="en-US,en;q=0.9",
))

# Use the header in your requests
headers = {
    "x-is-human": header,
    # ... other headers
}
```

### Script Path Extraction

Extract **Kasada script paths** from blocked pages (HTTP 429):

```python
from hyper_sdk.kasada import parse_kasada_script_path

script_path = parse_kasada_script_path(blocked_page_html)
# Returns: /ips.js?timestamp=...
```

## 🎯 DataDome Solutions

Solve **DataDome captchas** including slider challenges and interstitial pages.

### Interstitial Challenge Solving

Bypass **DataDome interstitial pages**:

```python
from hyper_sdk import DataDomeInterstitialInput

result = session.generate_interstitial_payload(DataDomeInterstitialInput(
    # interstitial input fields
))

payload = result["payload"]
headers = result["headers"]
# POST payload to https://geo.captcha-delivery.com/interstitial/
```

### Slider Captcha Solving

Solve **DataDome slider captchas** automatically:

```python
from hyper_sdk import DataDomeSliderInput

result = session.generate_slider_payload(DataDomeSliderInput(
    # slider input fields
))

check_url = result["payload"]
headers = result["headers"]
# GET request to check_url
```

### Tags Payload Generation

Generate **DataDome tags payload**:

```python
from hyper_sdk import DataDomeTagsInput

tags_payload = session.generate_tags_payload(DataDomeTagsInput(
    # tags input fields
))
```

### DeviceLink URL Parsing

Extract **DataDome device check URLs** from blocked pages:

```python
from hyper_sdk.datadome import parse_interstitial_device_check_link, parse_slider_device_check_link

# Parse interstitial device links
device_link = parse_interstitial_device_check_link(
    html_content, 
    datadome_cookie, 
    referer_url
)

# Parse slider device links  
device_link = parse_slider_device_check_link(
    html_content, 
    datadome_cookie, 
    referer_url
)
```

### Challenge Script

DataDome sometimes serves a challenge page with the **challenge script in its own file** instead of inlining it in the page:

```html
<script defer src="https://ct.captcha-delivery.com/interstitial.1.33.0.202609141.js"></script>
```

It switches between the two forms per request, so check every challenge page. When the page uses a separate file, fetch it with your own client so the request keeps your proxy, TLS fingerprint and headers, then pass the body as `script`:

```python
from hyper_sdk import DataDomeInterstitialInput
from hyper_sdk.datadome import parse_challenge_script_url

script = ""
script_url = parse_challenge_script_url(html_content)
if script_url is not None:
    script = your_client.get(script_url).text

result = session.generate_interstitial_payload(DataDomeInterstitialInput(
    # other interstitial input fields
    html=html_content,
    script=script,  # empty when the page inlines the script
))
```

The same applies to `DataDomeSliderInput`. One helper covers both challenge types, since the captcha page uses the same tag. `script` is optional and leaving it empty keeps working.

## 📖 Documentation

For detailed documentation on how to use the SDK, including examples and API reference, please visit our documentation website:

[https://docs.justhyped.dev/](https://docs.justhyped.dev/)

### Getting Help

- Check our [documentation](https://docs.justhyped.dev)
- Join our [Discord community](https://discord.gg/akamai)

## 🤝 Contributing

If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## 📄 License

This SDK is licensed under the [MIT License](LICENSE).

---

**Keywords**: Python SDK, bot protection bypass, web scraping, Akamai bypass, Incapsula bypass, Kasada bypass, DataDome bypass, anti-bot, captcha solver, automation, reverse engineering, bot detection, web automation