def is_cookie_valid(cookie: str, request_count: int) -> bool:
    """
        Determines if the provided _abck cookie value is valid, based on Akamai Bot Manager's
        client-side stop signal mechanism using the given request count. If the result is true, the client is ADVISED
        to halt further sensor data submissions. Submitting further would still produce a valid cookie but is unnecessary.

        The stop signal mechanism in the Akamai Bot Manager's client-side script informs a client that the cookie received is
        valid and that any additional submissions are superfluous.

        Args:
            cookie (str): The _abck cookie value.
            request_count (int): The number of requests made.

        Returns:
            bool: True if the cookie is valid, False otherwise.
    """
    parts = cookie.split("~")
    if len(parts) < 2:
        return False

    try:
        request_threshold = int(parts[1])
    except ValueError:
        request_threshold = -1

    return request_threshold != -1 and request_count >= request_threshold


def is_cookie_invalidated(cookie: str) -> bool:
    """
        Determines if the current session requires more sensors to be sent.

        Protected endpoints can invalidate a session by setting a new _abck cookie that ends in '~0~-1~-1' or similar.
        This function returns if such an invalidated cookie is present, if it is present you should be able to make the
        cookie valid again with only 1 sensor post.

        Args:
            cookie (str): The _abck cookie value.

        Returns:
            bool: True if the cookie has been invalidated, False otherwise.
    """
    parts = cookie.split("~")
    if len(parts) < 4:
        return False

    try:
        signal = int(parts[3])
    except ValueError:
        signal = -1

    return signal > -1
