class SensorInput:
    def __init__(self, abck: str, bmsz: str, version: str, page_url: str, user_agent: str, script_hash=""):
        self.abck = abck
        self.bmsz = bmsz
        self.version = version
        self.page_url = page_url
        self.user_agent = user_agent
        self.script_hash = script_hash


class PixelInput:
    def __init__(self, user_agent: str, html_var: str, script_var: str):
        self.user_agent = user_agent
        self.html_var = html_var
        self.script_var = script_var
