class PayloadInput:
    def __init__(self, user_agent: str, page_url: str, fp_url: str, ip: str, accept_language: str, script: str):
        """
        Creates a new PayloadInput instance for generating TrustDecision payloads.

        Args:
            user_agent (str): The userAgent that you're using for the entire session
            page_url (str): The target page URL where TrustDecision protection is active
            fp_url (str): The td-fp URL where the payload is posted
            ip (str): The IP address that will be used to post the sensor data to the target site
            accept_language (str): Your accept-language header value
            script (str): The TrustDecision fingerprinting script source code obtained from the fm.js endpoint
        """
        self.user_agent = user_agent
        self.page_url = page_url
        self.fp_url = fp_url
        self.ip = ip
        self.accept_language = accept_language
        self.script = script


class DecodeInput:
    def __init__(self, result: str, request_id: str):
        """
        Creates a new DecodeInput instance for decoding TrustDecision session keys.

        Args:
            result (str): The result field from TrustDecision's fingerprinting endpoint response
            request_id (str): The requestId field from TrustDecision's fingerprinting endpoint response
        """
        self.result = result
        self.request_id = request_id


class SignatureInput:
    def __init__(self, client_id: str, path: str):
        """
        Creates a new SignatureInput instance for generating TrustDecision session signatures.

        Args:
            client_id (str): The client ID returned from the payload generation endpoint
            path (str): The API endpoint path that will be called. This should match the value used in the td-session-path header of your actual request.
        """
        self.client_id = client_id
        self.path = path