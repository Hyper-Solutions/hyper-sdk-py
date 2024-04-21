import re

pixel_html_expr = re.compile(r'bazadebezolkohpepadr="(\d+)"')
pixel_script_url_expr = re.compile(r'src="(https?://.+/akam/\d+/\w+)"')
pixel_script_var_expr = re.compile(r'g=_\[(\d+)]')
pixel_script_string_array_expr = re.compile(r'var _=\[(.+?)];')
pixel_script_strings_expr = re.compile(r'("[^",]*")')


def parse_pixel_html_var(src: str) -> int:
    """
        ParsePixelHtmlVar gets the required pixel challenge variable from the given HTML code src.

        Args:
            src (str): HTML source code as a string.

        Returns:
            int: The parsed pixel HTML variable.

        Raises:
            Exception: If the pixel HTML var is not found in the source.
    """
    match = pixel_html_expr.search(src)
    if match:
        return int(match.group(1))
    else:
        raise Exception("hyper-sdk: pixel HTML var not found")


def parse_pixel_script_url(src: str) -> tuple[str, str]:
    """
        ParsePixelScriptURL gets the script URL of the pixel challenge script and the URL
        to post a generated payload to from the given HTML code src.

        Args:
            src (str): HTML source code as a string.

        Returns:
            tuple[str, str]: A tuple containing the script URL and the post URL.

        Raises:
            Exception: If the script URL is not found in the source.
    """
    match = pixel_script_url_expr.search(src)
    if match:
        script_url = match.group(1)
        # Create post_url
        parts = script_url.split("/")
        parts[-1] = "pixel_" + parts[-1]
        post_url = "/".join(parts)
        return script_url, post_url
    else:
        raise Exception("hyper-sdk: script URL not found")


def parse_pixel_script_var(src: str) -> str:
    """
        Gets the dynamic value from the pixel script.

        Args:
            src (str): HTML source code as a string.

        Returns:
            str: The dynamic value extracted from the pixel script.

        Raises:
            Exception: If the script variable is not found or if there are issues extracting it.
    """
    index_match = pixel_script_var_expr.search(src)
    if not index_match:
        raise Exception("hyper-sdk: script var not found")
    string_index = int(index_match.group(1))

    array_declaration_match = pixel_script_string_array_expr.search(src)
    if not array_declaration_match:
        raise Exception("hyper-sdk: script var not found")

    raw_strings = pixel_script_strings_expr.findall(array_declaration_match.group(1))
    if string_index >= len(raw_strings):
        raise Exception("hyper-sdk: script var not found")

    string_value = raw_strings[string_index].strip('"')
    return string_value
