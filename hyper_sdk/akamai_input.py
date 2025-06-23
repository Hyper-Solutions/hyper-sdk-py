class SensorInput:
    def __init__(self, abck: str, bmsz: str, version: str, page_url: str, user_agent: str, ip: str, acceptLanguage: str, context: str, script_hash="", dynamic_values=""):
        self.abck = abck
        self.bmsz = bmsz
        self.version = version
        self.page_url = page_url
        self.user_agent = user_agent
        self.script_hash = script_hash
        self.dynamic_values = dynamic_values
        self.context = context
        self.ip = ip
        self.acceptLanguage = acceptLanguage


class PixelInput:
    def __init__(self, user_agent: str, html_var: str, script_var: str, acceptLanguage: str, ip: str):
        self.user_agent = user_agent
        self.html_var = html_var
        self.script_var = script_var
        self.acceptLanguage = acceptLanguage
        self.ip = ip


class DynamicInput:
    def __init__(self, script: str):
        self.script = script


class SbsdInput:
    def __init__(self, index: int, user_agent: str, uuid: str, page_url: str, o_cookie: str, script: str, acceptLanguage: str, ip: str):
        self.index = index
        self.user_agent = user_agent
        self.uuid = uuid
        self.page_url = page_url
        self.o_cookie = o_cookie
        self.script = script
        self.acceptLanguage = acceptLanguage
        self.ip = ip
