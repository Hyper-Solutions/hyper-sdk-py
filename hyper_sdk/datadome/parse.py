import json
import re
from typing import Optional
from urllib.parse import urlencode

# Matches the tag a challenge page uses to load the bundle from
# ct.captcha-delivery.com, capturing the URL. The name in front of the version
# is left open so it keeps matching whatever DataDome calls the bundle, e.g.
# interstitial.1.33.0.202609141.js or captcha.1.34.0.202609141.js.
_CHALLENGE_SCRIPT_REGEX = re.compile(
    r"""<script[^>]+src\s*=\s*["']([^"']*/[a-z_-]+\.\d+\.\d+\.\d+\.[^"']*\.js)["']"""
)


def parse_slider_device_check_link(src: str, datadome_cookie: str, referer: str) -> str:
    """
        Parse the device check URL for DataDome slider captcha from a blocked response body.

        This function extracts the necessary parameters from the DataDome JavaScript object
        embedded in the HTML source and constructs the URL for the slider captcha challenge.

        Args:
            src (str): The HTML source of the blocked page containing the DataDome JavaScript object.
            datadome_cookie (str): The current value of the 'datadome' cookie.
            referer (str): The referer URL to be included in the device check link.

        Returns:
            str: The constructed device check URL for the slider captcha.

        Raises:
            RuntimeError: If the dd object cannot be extracted or parsed,
                          or if the proxy is blocked (indicated by 't' == 'bv').
    """
    try:
        dd_object = src.split("var dd=")[1].split("</script>")[0]
        dd_object = dd_object.replace("'", '"')
        dd_object_parsed = json.loads(dd_object)
    except Exception as _:
        raise RuntimeError("Failed to parse dd object.")

    if dd_object_parsed.get("t") == "bv":
        raise RuntimeError("proxy blocked")

    params = {
        "initialCid": dd_object_parsed.get("cid"),
        "hash": dd_object_parsed.get("hsh"),
        "cid": datadome_cookie,
        "t": dd_object_parsed.get("t"),
        "referer": referer,
        "s": str(dd_object_parsed.get("s")),
        "e": dd_object_parsed.get("e"),
        "dm": "cd",
    }

    return f"https://geo.captcha-delivery.com/captcha/?{urlencode(params)}"


def parse_interstitial_device_check_link(src: str, datadome_cookie: str, referer: str) -> str:
    """
        Parse the device check URL for DataDome interstitial challenge from a blocked response body.

        This function extracts the necessary parameters from the DataDome JavaScript object
        embedded in the HTML source and constructs the URL for the interstitial challenge.

        Args:
            src (str): The HTML source of the blocked page containing the DataDome JavaScript object.
            datadome_cookie (str): The current value of the 'datadome' cookie.
            referer (str): The referer URL to be included in the device check link.

        Returns:
            str: The constructed device check URL for the interstitial challenge.

        Raises:
            RuntimeError: If the DataDome dd object cannot be extracted or parsed.
    """
    try:
        dd_object = src.split("var dd=")[1].split("</script>")[0]
        dd_object = dd_object.replace("'", '"')
        dd_object_parsed = json.loads(dd_object)
    except Exception as _:
        raise RuntimeError("Failed to parse dd object.")

    params = {
        "initialCid": dd_object_parsed.get("cid"),
        "hash": dd_object_parsed.get("hsh"),
        "cid": datadome_cookie,
        "referer": referer,
        "s": str(dd_object_parsed.get("s")),
        "e": str(dd_object_parsed.get("e")),
        "b": str(dd_object_parsed.get("b")),
        "dm": "cd",
    }

    return f"https://geo.captcha-delivery.com/interstitial/?{urlencode(params)}"


def parse_challenge_script_url(html: str) -> Optional[str]:
    """
        Return the challenge bundle URL a device check or captcha page loads with a
        <script defer src="..."> tag, or None when the page has no such tag.

        DataDome serves some challenge pages with the bundle inlined in the HTML and
        others with it in its own file, switching between the two per request, so this
        has to be checked on every challenge rather than configured once.

        When it returns a URL, GET that URL with the same client, proxy and headers you
        used for the challenge page, and pass the response body as the `script` field of
        DataDomeInterstitialInput or DataDomeSliderInput. When it returns None the
        bundle is already in the HTML and `script` stays empty.

        Args:
            html (str): The response body of the GET request to the device check link.

        Returns:
            Optional[str]: The challenge bundle URL, or None when the page inlines it.

        Example:
            device_link = parse_interstitial_device_check_link(body, cookie, referer)
            # ... GET device_link with your own client, read the body into html ...

            script = ""
            script_url = parse_challenge_script_url(html)
            if script_url is not None:
                # fetch script_url with your own client, read the body into script
                script = your_client.get(script_url).text

            result = session.generate_interstitial_payload(DataDomeInterstitialInput(
                user_agent=user_agent,
                device_link=device_link,
                html=html,
                accept_language=accept_language,
                ip=ip,
                script=script,
            ))
    """
    match = _CHALLENGE_SCRIPT_REGEX.search(html)
    if match is None:
        return None

    return match.group(1)
