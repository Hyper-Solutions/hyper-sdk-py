import re
import random

# Precompiled regular expressions
script_regex = re.compile(r'src="(/_Incapsula_Resource\?[^"]*)"')


def parse_utmvc_script_path(script_content: str) -> str:
    """
        Parses the UTMVC script path from the given script content.

        This function searches the provided script content for a specific pattern matching the UTMVC script path
        using a precompiled regular expression. It extracts and returns the first match if found.

        Args:
            script_content (str): The content of the script from which the UTMVC script path is to be extracted.

        Returns:
            str: The extracted UTMVC script path.

        Raises:
            Exception: If the UTMVC script path is not found in the script content.
    """
    match = script_regex.search(script_content)
    if match:
        return match.group(1)
    else:
        raise Exception("hyper-sdk: utmvc script not found")


def get_utmvc_submit_path() -> str:
    """
        Generates a UTMVC submit path with a unique random query parameter.

        This function constructs a submit path for the UTMVC script by appending a random floating-point number as a query
        parameter. The random number is used to ensure uniqueness of the request.

        Returns:
            str: A unique UTMVC submit path.
    """
    random_float = random.random()
    return f"/_Incapsula_Resource?SWKMTFSR=1&e={random_float:g}"
