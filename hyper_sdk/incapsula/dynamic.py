import re
from urllib.parse import urlparse

# Precompiled regular expressions
reese_script_regex = re.compile(r'src\s*=\s*"((/[^/]+/\d+)(?:\?.*)?)"')


def parse_dynamic_reese_script(html_content: str, url_str: str) -> tuple[str, str]:
    """
    Parses the sensor path and script path from the given HTML content.

    This function searches the provided HTML for a script element containing a specific pattern
    and extracts both the sensor path (shortened path) and script path (the full path).
    It requires that the HTML contains "Pardon Our Interruption" to confirm it's the correct page type.
    It also takes a URL string, extracts the hostname, and appends it to the sensor path.

    Args:
        html_content (str): The HTML content to parse.
        url_str (str): The URL string to extract the hostname from.

    Returns:
        tuple[str, str]: A tuple containing the sensor path (with hostname) and script path.

    Raises:
        ValueError: If the URL is invalid.
        Exception: If the page is not an interruption page or if the Reese script is not found.
    """
    # Parse the URL to extract hostname
    try:
        parsed_url = urlparse(url_str)
        hostname = parsed_url.netloc
    except Exception:
        raise ValueError("hyper-sdk: invalid URL")

    # Verify this is an interruption page
    if "Pardon Our Interruption" not in html_content:
        raise Exception("hyper-sdk: not an interruption page")

    # Find the Reese script
    match = reese_script_regex.search(html_content)
    if not match or len(match.groups()) < 2:
        raise Exception("hyper-sdk: reese script not found")

    script_path = match.group(1)
    sensor_path = match.group(2)

    # Append the hostname to the sensor path
    return f"{sensor_path}?d={hostname}", script_path