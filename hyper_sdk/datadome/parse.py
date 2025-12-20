import json
from urllib.parse import urlencode


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
