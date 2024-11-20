class SensorInput:
    def __init__(self, abck: str, bmsz: str, version: str, page_url: str, user_agent: str, ip = "", language = "", script_hash="", dynamic_values=""):
        self.abck = abck
        self.bmsz = bmsz
        self.version = version
        self.page_url = page_url
        self.user_agent = user_agent
        self.script_hash = script_hash
        self.dynamic_values = dynamic_values
        self.ip = ip
        self.language = language


class PixelInput:
    def __init__(self, user_agent: str, html_var: str, script_var: str):
        self.user_agent = user_agent
        self.html_var = html_var
        self.script_var = script_var


class DynamicInput:
    def __init__(self, script: str):
        self.script = script


class SbsdInput:
    def __init__(self, user_agent: str, uuid: str, page_url: str, o_cookie: str, script_hash = "", language = "", ip = ""):
        self.user_agent = user_agent
        self.uuid = uuid
        self.page_url = page_url
        self.o_cookie = o_cookie
        self.script_hash = script_hash
        self.language = language
        self.ip = ip
