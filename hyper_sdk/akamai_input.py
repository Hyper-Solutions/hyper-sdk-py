class SensorInput:
    def __init__(self, abck: str, bmsz: str, version: str, page_url: str, user_agent: str, ip: str, accept_language: str,
                 context: str, script: str, script_url: str):
        self.abck = abck
        self.bmsz = bmsz
        self.version = version
        self.page_url = page_url
        self.user_agent = user_agent
        self.script = script
        self.script_url = script_url
        self.context = context
        self.ip = ip
        self.accept_language = accept_language


class TelemetryInput(SensorInput):
    def __init__(self, abck: str, bmsz: str, page_url: str, user_agent: str, ip: str, accept_language: str,
                 context: str, script: str, script_url: str, j: str = ""):
        # A sensor request for a site that sends an Akamai-BM-Telemetry header on
        # its protected API calls instead of posting sensor data. Only v3 dynamic
        # scripts send the header, so there is no version. script and context
        # chain across headers the same way they do across sensor posts.
        super().__init__(abck, bmsz, "", page_url, user_agent, ip, accept_language, context, script, script_url)
        # j is the "j" from the response of the site's get_params request (see
        # get_telemetry_params), sent as it was returned. Leave it empty when the
        # site makes no get_params request.
        self.j = j


class TelemetryParamsInput:
    def __init__(self, page_url: str, script: str = "", context: str = ""):
        self.page_url = page_url
        # script is mutually exclusive with context, a context returned by an
        # earlier telemetry or telemetry params request.
        self.script = script
        self.context = context


class PixelInput:
    def __init__(self, user_agent: str, html_var: str, script_var: str, accept_language: str, ip: str):
        self.user_agent = user_agent
        self.html_var = html_var
        self.script_var = script_var
        self.accept_language = accept_language
        self.ip = ip


class SbsdInput:
    def __init__(self, user_agent: str, uuid: str, page_url: str, o_cookie: str, script: str,
                 accept_language: str, ip: str, context: str = "", script_url: str = ""):
        self.user_agent = user_agent
        self.uuid = uuid
        self.page_url = page_url
        self.o_cookie = o_cookie
        # script is mutually exclusive with context. The first sbsd request should
        # include script; subsequent requests should only include context. A hard
        # block (an sbsd POST with a t parameter) always sends script and an empty
        # context, never the context from an earlier request.
        self.script = script
        self.accept_language = accept_language
        self.ip = ip
        self.context = context
        # script_url is the absolute src of the SBSD script tag, query included.
        # Optional: when set, the fingerprint's resource-timing signal carries the
        # script's own entry the way a browser's does.
        self.script_url = script_url
