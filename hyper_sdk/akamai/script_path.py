import re

# Precompiled regular expressions
script_path_expr = re.compile(r'<script type="text/javascript"\s+(?:nonce=".*?")?\s+src="([a-z\d/\-_]+)"></script>',
                              re.IGNORECASE)


def parse_script_path(src: str) -> str:
    """
        Gets the Akamai Bot Manager web SDK path from the given HTML code src.

        This function searches the provided HTML source code for the path of a JavaScript script tag that matches the
        specified regular expression pattern.

        Args:
            src (str): The HTML source code as a string.

        Returns:
            str: The path of the script extracted from the script tag.

        Raises:
            Exception: If the script path is not found in the source.
    """
    match = script_path_expr.search(src)
    if match:
        return match.group(1)
    else:
        raise "hyper-sdk: script path not found"
